class Database {
    constructor() {
        this.responses = {};
    }

    addResponse(input, response) {
        // Add a new response to the database
        this.responses[input] = response;
    }

    getResponse(input) {
        // Retrieve a response from the database
        return this.responses[input];
    }
}
