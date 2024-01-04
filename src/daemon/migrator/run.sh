echo "starting migrator"

# Ensure the dependencies are met
go mod tidy
# Build the app
go build .

# Run the daemon
./migrator
