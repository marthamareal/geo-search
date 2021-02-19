import React from 'react';
import '../node_modules/bootstrap/dist/css/bootstrap.min.css';
import './App.css';
import {BrowserRouter as Router, Switch, Route, Link} from "react-router-dom";
import Login from "./components/Login";
import Signup from "./components/Signup";
import Home from "./components/Home";

function App() {
    return (
        <Router>
            <div className="App">
                <nav className="navbar navbar-expand-lg navbar-light fixed-top">
                    <div className="container">
                        <Link className="navbar-brand" to={"/"}>GeoSearch</Link>
                    </div>
                </nav>
                <Switch>
                    <Route exact path='/' component={Home}/>
                    <Route path="/sign-in" component={Login}/>
                    <Route path="/sign-up" component={Signup}/>
                </Switch>
            </div>
        </Router>
    );
}

export default App;