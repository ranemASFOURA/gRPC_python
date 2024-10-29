# addition_service.py
import grpc
from concurrent import futures
import calculator_pb2
import calculator_pb2_grpc

# Define the AdditionService servicer (implementation)
class AdditionServiceServicer(calculator_pb2_grpc.AdditionServiceServicer):
    def Add(self, request, context):
        # Perform addition
        result = request.num1 + request.num2
        return calculator_pb2.CalculationResponse(result=result)

# Create the gRPC server
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    calculator_pb2_grpc.add_AdditionServiceServicer_to_server(AdditionServiceServicer(), server)
    server.add_insecure_port('[::]:50051')  # Listen on port 50051
    server.start()
    print("AdditionService is running on port 50051...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
