import asyncio



async def suma(q):
    n = await q.get()
    rezultat = (n * (n + 1)) / 2
    print(f"Suma pentru {n}: {rezultat}")
    q.task_done()


async def ex1():
    q = asyncio.Queue()

    for val in [5, 2, 3, 4]:
        await q.put(val)
    for _ in range(4):

        asyncio.create_task(suma(q))

    await q.join()


if __name__ == "__main__":
    asyncio.run(ex1())




