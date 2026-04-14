import random
import asyncio
import time

queue = asyncio.Queue(5) # At most 5 items in the queue

async def producer(): # `async` 让我们可以在里面用 `await` 来等别的 function return 之后在继续往下
    """
    Async-ly put 10 items into the queue, every 2 seconds for 5 times.
    """
    for _ in range(10):
        time_cost = random.randint(1, 3)
        print(f'Produced {time_cost}')
        await queue.put(time_cost) # NOTE: .put() 可以 await, 这样queue满的时候, func会在这里停住, 直到queue有空位
    
    return 'Producer done!' # 这个return的值会被 `await producer()` 的地方拿到


async def consumer():
    """
    Async-ly get items from the queue, and run them for `time_cost` seconds.
    """
    while True:
        time_cost = await queue.get() # NOTE: .get() 可以 await, 这样queue空的时候, func会在这里停住, 直到queue有新item
        print(f'Consumed {time_cost}')
        await asyncio.sleep(time_cost) # 打住, 等return (模拟花一些时间来做某个task)
        queue.task_done() # 外面有一个 .join() 在等着 queue 里面所有的item都被task_done()了, 才会继续往下走

if __name__ == "__main__":
    print('Start add & get tasks...')
    start_time = time.time()

    loop = asyncio.get_event_loop()
    loop.create_task(producer()) # 让producer开始执行, 但是不等它return
    
    # Create three workers to consume from the queue concurrently
    tasks = []
    for _ in range(3): 
        tasks.append(loop.create_task(consumer())) # 记录这三个consumer的task
    
    # 因为 .get() 会把 queue 中的 item 拿走, 此时 queue 虽然为空, 但是 被拿走的 item 不一定 finished 了
    # 所以这里我们用 join() 来block, join() 会等到 queue 中的 item 都被 marked task_done() 了之后, 才会 return.
    loop.run_until_complete(queue.join()) # wait 直到所有被拿走的 item 全都 marked as done 

    # Cancel the consumer tasks after queue is empty
    for task in tasks:
        task.cancel()

    end_time = time.time()
    print(f'All tasks done! Finished in {end_time - start_time:.2f} seconds.')
