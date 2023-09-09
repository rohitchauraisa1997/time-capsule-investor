import Button from '@mui/material/Button';
import TextField from "@mui/material/TextField";
import {Card, Typography} from "@mui/material";
import {useState} from "react";
import {useNavigate} from "react-router-dom";
import axios from 'axios';

function Signup() {
    const [username, setUsername] = useState("")
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")
    const navigate = useNavigate()

    const [errorMessage, setErrorMessage] = useState(null); 

    const handleSignupClick = () =>{
        setErrorMessage(""); // Clear previous error message
        console.log("handleSignupClick triggered");
        axios.post("http://localhost:3000/user/signup", {
            email:email,
            username: username,
            password: password
        }).then(response=>{
            console.log(response);
            return response.data
        })
        .then(data=>{
            console.log(data);
            navigate("/signin")
        })
        .catch(error=>{
            console.error("Error during signup ", error);
            console.error("Error during signup ", error.response.data);
            console.error("Error during signup ", error.response.data.detail);
            // window.alert("Error during signup ", error)
            const errorMessage = error.response.data.detail
            setErrorMessage(`Error: ${errorMessage}`);
        })
    }

    return <div>    
            <div style={{
                paddingTop: 150,
                marginBottom: 10,
                display: "flex",
                justifyContent: "center"
            }}>
                <Typography variant={"h6"}>
                Welcome to Time Capsule Investor. Sign up below
                </Typography>
            </div>
        <div style={{display: "flex", justifyContent: "center"}}>
            <Card varint={"outlined"} style={{width: 400, padding: 20}}>

                <TextField
                    onChange={(event) => {
                        let elemt = event.target;
                        setUsername(elemt.value);
                    }}
                    fullWidth={true}
                    label="Username"
                    variant="outlined"
                />
                <br/><br/>

                <TextField
                    onChange={(event) => {
                        let elemt = event.target;
                        setEmail(elemt.value);
                    }}
                    fullWidth={true}
                    label="Email"
                    variant="outlined"
                />
                <br/><br/>

                <TextField
                    onChange={(e) => {
                        setPassword(e.target.value);
                    }}
                    fullWidth={true}
                    label="Password"
                    variant="outlined"
                    type={"password"}
                />
                <br/><br/>

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
                    onClick={handleSignupClick}
                > Signup</Button>
            </Card>
        </div>
    </div>
}

export default Signup;