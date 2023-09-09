db = db.getSiblingDB("bucket_gains_tracker_mongodb");
db.createUser({
  user: "bucket-user",
  pwd: "bucket-pwd",
  roles: [
    {
      role: "readWrite",
      db: "bucket_gains_tracker_mongodb",
    },
    {
      role: "dbAdmin",
      db: "bucket_gains_tracker_mongodb",
    },
  ],
});
