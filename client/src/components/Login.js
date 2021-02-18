import React, { Component } from "react";
import {axiosInstance} from "../base";

 class Login extends Component {
     constructor(props) {
         super(props);
         this.state ={
             email: '',
             password: ''
         }
     }
     onChange = event => {
        switch (event.target.id) {
          case "email":
              this.setState({email: event.target.value})
            break;
          case "password":
            this.setState({ password: event.target.value });
            break;
          default:
            break;
        }
      };
     onSubmit = async event => {
         const form_data = {
             'email': this.state.email,
             'password': this.state.password
         }
    event.preventDefault();
    await axiosInstance
        .post("/api/users/login/", form_data)
        .then(response => {
          localStorage.setItem("access", response.data.access);
          localStorage.setItem("user_id", response.data.id);
        })
        .catch(error => {
            if (error.response?.data?.detail){
               window.alert(error.response?.data?.detail)
            }
            window.alert("Login failed")
        });
  };

    render(){
        return (
            <form onSubmit={this.onSubmit}>
                <h3>Sign In</h3>

                <div className="form-group">
                    <label>Email address</label>
                    <input
                        id='email'
                        type="email"
                        className="form-control"
                        placeholder="Enter email"
                        onChange={this.onChange}
                        value={this.state.email}
                        required
                    />
                </div>

                <div className="form-group">
                    <label>Password</label>
                    <input
                        id='password'
                        type="password"
                        className="form-control"
                        placeholder="Enter password"
                        onChange={this.onChange}
                        value={this.state.password}
                        required
                    />
                </div>

                <button type="submit" className="btn btn-primary btn-block">Submit</button>
                <p className="register text-right">
                    Don't have an account? <a href="/sign-up">Sign Up</a>
                </p>
            </form>
        );
    }
}

export default Login;