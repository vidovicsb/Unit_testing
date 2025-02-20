import asyncio      # Module to handle asynchronous processes
import unittest     # Module for unit testing


class TestAsyncio(unittest.IsolatedAsyncioTestCase):        # IsolatedAsyncioTestCase is special to asyncio testing
    
    async def async_func(self):                             # async def declares an asynchronous function
        """An async function that returns a value."""
        await asyncio.sleep(0.2)                            # async.sleep() does not pause the entire event loop like time.sleep()
        return "Hello"
    
    async def simple_task(self, value, delay):
        """Same as async_func, but with modifiable parameters."""
        await asyncio.sleep(delay)
        return value
    
    async def faulty_task(self):
        """Function to raise an error."""
        await asyncio.sleep(0.1)
        raise ValueError("Intentional Error")
    
    async def slow_function(self):
        await asyncio.sleep(2)
        
    async def async_run(self):
        """A simple async function."""
        return 10
    
    async def test_async_function(self):
        """Checks if async function runs correctly."""
        result = await self.async_func()
        self.assertEqual(result, "Hello")
        
    async def test_create_task(self):
        """Checks if asyncio.create_task runs correctly."""
        task1 = asyncio.create_task(self.simple_task('Hello1', 0.1))
        task2 = asyncio.create_task(self.simple_task('Hello2', 0.2))
        
        # Store the results from the tasks
        result1 = await task1
        result2 = await task2
        
        # Check if results are equal to the expected values
        self.assertEqual(result1, 'Hello1')
        self.assertEqual(result2, 'Hello2')
        
    async def test_gather(self):
        """Check if asyncio.gather() works correctly."""
        # Store results from tasks in a list called results
        results = await asyncio.gather(
            self.simple_task('A', 0.1),
            self.simple_task('B', 0.2),
            self.simple_task('C', 0.3)
        )
        
        # Check if list results equal to the expected values
        self.assertEqual(results, ['A', 'B', 'C'])
        
    async def test_exception_raised(self):
        """Checks if a raised error is handled properly."""
        with self.assertRaises(ValueError):
            await self.faulty_task()

    async def test_exception_in_create_task(self):
        """Checks if an error in create task is handled properly."""
        task = asyncio.create_task(self.faulty_task())
        
        try:
            await task
        except ValueError as e:
            self.assertEqual(str(e), 'Intentional Error')
            
    async def test_timeout_handling(self):
        """Check if asyncio.wait_for() raises timeout error."""
        with self.assertRaises(asyncio.TimeoutError):
            # Wait 1 sec before raising timeout error
            await asyncio.wait_for(self.slow_function(), timeout=1)
            
    def test_async_run(self):
        """Check if async.run() works properly."""
        result = asyncio.run(self.async_run())
        self.assertEqual(result, 10)
    
            

if __name__ == '__main__':
    unittest.main()