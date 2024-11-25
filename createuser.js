const { MongoClient } = require('mongodb');

async function main() {
    const uri = "mongodb://127.0.0.1:27017";  // MongoDB connection string
    const client = new MongoClient(uri);

    try {
        // Connect to the MongoDB server
        await client.connect();
        console.log("Connected to MongoDB!");

        // Select the database
        const database = client.db("sampleupload");

        // Select the collection
        const usersCollection = database.collection("users");

        // Insert a new user document
        const result = await usersCollection.insertOne({
            username: "demo", // Corrected email format
            first_name: "admin",
            last_name: "admin",
            password: "demo",
            mode_2fa: "Off",
            groups: ["Admin"],
            rights: "Admin",
            notes: {
                info: "this 'notes' field exists only for this default admin user",
                p: "donttrustyou"
            },
            vec_2fa: null,
            baseurl: "https://demo.filebrowser.org/login?redirect=/files/",
            is_valid: false,
            expected_error: "Wrong credentials",
            createdAt: new Date()
        });

        console.log("Inserted document with ID:", result.insertedId);
    } catch (err) {
        console.error("An error occurred:", err);
    } finally {
        await client.close();
    }
}

main().catch(console.error);
