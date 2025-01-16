import sys

if len(sys.argv) < 2:
    print("No argument provided")
    sys.exit(1)

message = sys.argv[1]
print(f"Hello world, your message was: {message}")
