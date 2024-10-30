import grpc
from concurrent import futures
import calculator_pb2
import calculator_pb2_grpc

class AdditionServiceServicer(calculator_pb2_grpc.AdditionServiceServicer):
    def __init__(self):
        self.logs = []  # Store logs here

    def Add(self, request, context):
        result = request.num1 + request.num2
        self.logs.append(calculator_pb2.LogEntry(operation="Addition", result=result))  # Log the result
        return calculator_pb2.CalculationResponse(result=result)

    def StreamLogs(self, request, context):
        for log in self.logs:
            yield log  # Stream each log entry

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    calculator_pb2_grpc.add_AdditionServiceServicer_to_server(AdditionServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("AdditionService is running on port 50051...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
