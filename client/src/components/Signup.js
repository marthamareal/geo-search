import React, { Component } from "react";
import {axiosInstance} from "../base";

 class Signup extends Component {
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
        .post("/api/users/signup/", form_data)
        .then(response => {
          console.log(response.data)
            window.alert(response.data.message)
        })
        .catch(error => {
            if (error.response?.data?.error){
               window.alert(error.response?.data?.error[0])
            }
            if (error.response?.data?.email){
                window.alert(error.response?.data?.email[0])
            }
            window.alert("Registration failed")
        })
  };

    render(){
        return (
            <div className="auth-wrapper">
        <div className="auth-inner">
            <form onSubmit={this.onSubmit}>
                <h3>Sign Up</h3>

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
                    Already registered <a href="/sign-in">sign in?</a>
                </p>
            </form>
        </div>
            </div>
        );
    }
}

export default Signup;