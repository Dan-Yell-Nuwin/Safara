# Queue Service

## Testing

To test the system, download both the python files in the same directory:
- Run the main in the 'QueueRunner.py' or simply just run the rile.
- Then run the 'QueueTest.py' file by running either the main or the file
- To add more tests, add to the method TestFlaskAPI to run the unit tests.
- IMPORTANT: Make sure you always run 'QueueRunner.py' before running 'QueueTest.py' each time.
Otherwise, the tests would not pass and some of the data may be misleading to fail some cases.
- Note: The server runs on http://localhost:5000

## More Time
- Instead of using a dictionary to store the queuenames and all the messages,
it would have been more scaleable to use a db such as sqlite to connect to and
make queries for each method.
- Would have also added more tests to test the robustness of each method of the program.
- Would have also added thread locking features to account for if two clients accessed the API at once.
