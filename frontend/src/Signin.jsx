import { useState } from "react";
import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";
import { Card, Typography } from "@mui/material";
import axios from "axios";

function Signin() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [errorMessage, setErrorMessage] = useState(null); 

    const handleSigninClick = () => {
    setErrorMessage(""); // Clear previous error message
    const formData = new FormData();
    formData.append("username", username);
    formData.append("password", password);

    axios.post("http://localhost:3000/user/signin", formData)
        .then((response) => {
            return response.data;
        })
        .then((data) => {
            const accessToken = data["access_token"];
            localStorage.setItem("token", accessToken);
            // TODO: Find a better way than window.location to render Appbar without reload.
            window.location = "/bucket/all?stockIndex=nasdaq";
            // navigate('/bucket/all');
        })
        .catch((error) => {
            if (error.response && error.response.status === 401) {
                console.error("Unauthorized: ", error);
                setErrorMessage("Wrong credentials.");
            } else {
                console.error("Error during signin", error);
                setErrorMessage("Error: ", error);
            }
        });
    };

return (
    <div>
        <div
            style={{
            paddingTop: 150,
            marginBottom: 10,
            display: "flex",
            justifyContent: "center",
            }}
        >
            <Typography variant={"h6"}>Welcome back. Sign in below</Typography>
        </div>
        <div style={{ display: "flex", justifyContent: "center" }}>
            <Card variant={"outlined"} style={{ width: 400, padding: 20 }}>
            <TextField
                onChange={(event) => {
                let elemt = event.target;
                setUsername(elemt.value);
                }}
                fullWidth={true}
                label="Username"
                variant="outlined"
            />
            <br />
            <br />

            <TextField
                fullWidth={true}
                id="outlined-basic"
                label="Password"
                variant="outlined"
                type={"password"}
                onChange={(e) => {
                setPassword(e.target.value);
                }}
            />
            <br />
            <br />

            {/* if errorMessage is not null '&&' helps rendering the error msg */}
            {errorMessage && (
                <Typography variant="body2" color="error">
                {errorMessage}
                </Typography>
            )}
            <br />
            
            <Button
                size={"large"}
                variant="contained"
                onClick={handleSigninClick}
                color="secondary"
            >
                Signin
            </Button>
            </Card>
        </div>
        </div>
    );
}

export default Signin;