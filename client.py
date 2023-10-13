import asyncio
import aiohttp



async def main():
    async with aiohttp.ClientSession() as session:
        #создание обьявления 

        response = await session.post(
            "http://127.0.0.1:8080/advertisements",
            json={"title": "airplane", 
                  "description": "papper airplane",
                  "creator": ""
                  },
        )
        json_data = await response.json()
        print(response.status)
        print(json_data)

        #запрос обьявления по id

        # response = await session.get(
        #      "http://127.0.0.1:8080/advertisements/2",
        # )
        # json_data = await response.json()
        # print(response.status)
        # print(json_data)
        
        #изменение обьявления
        
        # response = await session.patch(
        #    "http://127.0.0.1:8080/advertisements/2",
        #    json={"titly": "new_name"},
        # )
        # json_data = await response.json()
        # print(response.status)
        # print(json_data)
        
        
        #удаление обьявления

        # response = await session.delete(
        #     "http://127.0.0.1:8080/advertisements/1",
        # )
        # json_data = await response.json()
        # print(response.status)
        # print(json_data)

        # response = await session.get(
        #     "http://127.0.0.1:8080/advertisements/1",
        # )
        # json_data = await response.json()
        # print(response.status)
        # print(json_data)


if __name__ == "__main__":
    asyncio.run(main())
