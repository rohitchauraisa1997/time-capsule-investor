db = db.getSiblingDB("bucket_gains_tracker_mongodb");

db.createCollection("bucket-gains");
// db["bucket-gains"].insertMany([
//   {
//     bucket_name: "Bucket 1",
//     bucket_stocks: ["PIIND", "HDFC"],
//     created_at: new Date(),
//     updated_at: new Date(),
//   },
//   {
//     bucket_name: "Bucket 2",
//     bucket_stocks: ["IBM", "SONY", "MICROSOFT"],
//     created_at: new Date(),
//     updated_at: new Date(),
//   },
//   // Add more initial data here
// ]);
