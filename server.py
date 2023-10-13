import json
from aiohttp import web
from models import engine, Session, Advertisements, Base

from sqlalchemy.exc import IntegrityError

app = web.Application()


async def context_orm(app: web.Application):
    print("START")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()
    print("STOP")


@web.middleware
async def session_middleware(request: web.Request, handler):
    async with Session() as session:
        request["session"] = session
        response = await handler(request)
        return response


app.cleanup_ctx.append(context_orm)
app.middlewares.append(session_middleware)


def get_http_error(error_class, description: str):
    return error_class(
        text=json.dumps({"status": "error", "description": description}),
        content_type="application/json",
    )


async def get_advertisements(advertisements_id: int, session: Session):
    advertisements = await session.get(Advertisements, advertisements_id)
    if advertisements is None:
        raise get_http_error(web.HTTPNotFound, "Advertisements not found")
    return advertisements


async def add_advertisements(advertisements: Advertisements, session: Session):
    try:
        session.add(advertisements)
        await session.commit()
    except IntegrityError as er:
        raise get_http_error(web.HTTPConflict, "Advertisements already exists")
    return advertisements


class AdvertisementsView(web.View):
    @property
    def session(self):
        return self.request["session"]

    @property
    def advertisements_id(self):
        return int(self.request.match_info["advertisements_id"])

    async def get(self):
        advertisements = await get_advertisements(self.advertisements_id, self.session)
        return web.json_response(
            {
                "id": advertisements.id,
                "title": advertisements.title,
                "description": advertisements.description,
                "creation_time": advertisements.creation_time.isoformat(),
            }
        )

    async def post(self):
        json_validated = await self.request.json()
        advertisements = Advertisements(**json_validated)
        advertisements = await add_advertisements(advertisements, self.session)
        return web.json_response(
            {"id": advertisements.id, "title": advertisements.title}
        )

    async def patch(self):
        json_validated = await self.request.json()
        advertisements = await get_advertisements(self.advertisements_id, self.session)
        for field, value in json_validated.items():
            setattr(advertisements, field, value)
            advertisements = await add_advertisements(advertisements, self.session)
        return web.json_response(
            {
                "id": advertisements.id,
                "title": advertisements.title,
            }
        )

    async def delete(self):
        advertisements = await get_advertisements(self.advertisements_id, self.session)
        await self.session.delete(advertisements)
        await self.session.commit()
        return web.json_response(
            {
                "status": "success",
            }
        )


app.add_routes(
    [
        web.post("/advertisements", AdvertisementsView),
        web.get("/advertisements/{advertisements_id}", AdvertisementsView),
        web.patch("/advertisements/{advertisements_id}", AdvertisementsView),
        web.delete("/advertisements/{advertisements_id}", AdvertisementsView),
    ]
)


if __name__ == "__main__":
    web.run_app(app)
