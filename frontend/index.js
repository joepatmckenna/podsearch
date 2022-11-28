import express from "express";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const app = express();

app.use(express.static(path.join(__dirname, "dist")));

const port = process.env.PORT || 8080;
app.listen(port, () => {
  console.log("Hello world listening on port", port);
});
