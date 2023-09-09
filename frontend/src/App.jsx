import { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import BucketGainsAppBar from "./Appbar.jsx";
import BucketCards from "./Bucketcards.jsx"
import Signup from './Signup.jsx';
import Signin from './Signin.jsx';
import BucketInfo from './BucketInfo.jsx'
import AddBucket from './AddBucket.jsx';
import UpdateBucket from './UpdateBucket.jsx';
import StockChart from './RenderGraph.jsx';
import HomePage from './HomePage.jsx';
import axios from 'axios';

function App() {
    const [authenticated, setAuthenticated] = useState(false);

    useEffect(() => {
        // Use your authentication logic here
        axios.get("http://localhost:3000/user/me", {
            headers: {
                Authorization: "Bearer " + localStorage.getItem("token")
            }
        })
        .then(response => {
            setAuthenticated(true);
        })
        .catch(error => {
            setAuthenticated(false);
        });
    }, []);

    console.log("authenticated",authenticated);

    return (
        <div >
            <Router>
                <BucketGainsAppBar />
                <Routes>
                    <Route path={"/home"} element={<HomePage />} />
                    <Route path={"/signup"} element={<Signup />} />

                    {/* Only allow access to the signin route if not authenticated */}
                    {!authenticated && <Route path={"/signin"} element={<Signin />} />}
                    {/* If Authenticated user tries to go to signin route manually.. route him/her to HomePage */}
                    {authenticated && <Route path={"/signin"} element={<HomePage />} />}
                    
                    {/* Secure routes */}
                    {authenticated ? (
                        <>
                            <Route path={"/bucket/update"} element={<UpdateBucket />} />
                            <Route path={"/bucket/add"} element={<AddBucket />} />
                            <Route path={"/bucket/all"} element={<BucketCards />} />
                            <Route path={"/bucket/profit"} element={<BucketInfo />} />
                            <Route path={"/stock/render"} element={<StockChart />} />
                        </>
                    ) : null}

                    {/* Redirect to home if trying to access secure routes while not authenticated */}
                    {!authenticated && <Route path={"/*"} element={<HomePage />} />}
                </Routes>
            </Router>
        </div>
    );
}

export default App;
