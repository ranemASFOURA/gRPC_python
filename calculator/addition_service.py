import grpc  # Import gRPC library for server and client communication
from concurrent import futures  # Import futures for managing asynchronous operations
import calculator_pb2
import calculator_pb2_grpc

# Define the AdditionServiceServicer class that implements the AdditionService
class AdditionServiceServicer(calculator_pb2_grpc.AdditionServiceServicer):
    def __init__(self):
        # Initialize a list to store logs of operations performed
        self.logs = []

    # Define the Add method that handles addition requests
    def Add(self, request, context):

        result = request.num1 + request.num2
        # Log the operation and result in the logs list
        self.logs.append(calculator_pb2.LogEntry(operation="Addition", result=result))

        return calculator_pb2.CalculationResponse(result=result)

    # Define the StreamLogs method to allow clients to stream logs
    def StreamLogs(self, request, context):
        # Stream each log entry in the logs list to the client
        for log in self.logs:
            yield log  # Yield each log entry to the client

# Function to start and run the gRPC server
def serve():
    # Create a gRPC server with a thread pool executor for handling requests concurrently
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    calculator_pb2_grpc.add_AdditionServiceServicer_to_server(AdditionServiceServicer(), server)
    # Bind the server to port 50051 on all network interfaces
    server.add_insecure_port('[::]:50051')

    server.start()
    print("AdditionService is running on port 50051...")
    # Keep the server running and wait for incoming requests
    server.wait_for_termination()

# Entry point to start the server when the script is executed
if __name__ == '__main__':
    serve()
