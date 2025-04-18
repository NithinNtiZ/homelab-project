import httpx
import asyncio

async def post_request(url):
    async with httpx.AsyncClient() as client:
        # Send the request and await the response asynchronously
        response = await client.get(url)
        return response

async def handle_responses(response, index):
    # response = await task
    if response.status_code == 200:
        json_data = response.json()
        timestamp = json_data.get('dateTime')
        print(f"Task {index} - Server Timestamp: {timestamp}")
    else:
        print(f"Task {index} - Failed with status code: {response.status_code}")

async def main():
    url = 'https://timeapi.io/api/Time/current/zone?timeZone=UTC'
    
    for _ in range(10):  # Repeat the task block 10 times
        # Create two tasks for sending POST requests
        task1 = asyncio.create_task(post_request(url))
        task2 = asyncio.create_task(post_request(url))
        response1 = await task1
        response2 = await task2
        
        # Handle responses asynchronously and print them when they arrive with index
        await asyncio.gather(
            handle_responses(response1, 1),
            handle_responses(response2, 2)
        )
        print(f'------------------------------------------------')
        await asyncio.sleep(0.5)  # Wait for 500ms between each loop iteration

# Run the async function
if __name__ == '__main__':
    asyncio.run(main())