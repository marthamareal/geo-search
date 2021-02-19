import React, {Component} from "react";
import {axiosInstance} from "../base";

class Home extends Component {
    constructor(props) {
        super(props);
        this.state = {
            x: '',
            y: '',
            n: '',
            operation_type: 'nearest',
            search_results: [],
            search_history: []
        }
    }

    async componentDidMount() {
        await axiosInstance
            .get('/api/request_history/')
            .then(response => {
                this.setState({search_history: response.data})
            })
            .catch(error => {
                window.alert("Failed to get your search history")
            })
    }

    onChange = event => {
        switch (event.target.id) {
            case "x":
                this.setState({x: event.target.value})
                break;
            case "y":
                this.setState({y: event.target.value});
                break;
            case "n":
                this.setState({n: event.target.value});
                break;
            case "operation_type":
                this.setState({operation_type: event.target.value});
                break;
            default:
                break;
        }
    };

    onSubmit = async event => {
        event.preventDefault();
        await axiosInstance
            .get(`/api/points/get_locations?x=${this.state.x}&y=${this.state.y}&n=${this.state.n}&operation_type=${this.state.operation_type}`)
            .then(response => {
                this.setState({search_results: response.data})
            })
            .catch(error => {
                if (error.response?.data?.error) {
                    window.alert(error.response?.data?.error[0])
                }
                if (error.response?.data?.email) {
                    window.alert(error.response?.data?.email[0])
                }
                window.alert("Failed to get results")
            })
    };

    handleAutoInput = data => {
        this.setState({x: data.x})
        this.setState({y: data.y})
        this.setState({n: data.n})
        this.setState({operation_type: data.operation_type})
    }

    render() {
        return (
            localStorage.getItem("access") ?
                <div>
                    <div className="row home">
                    <div className="col-sm-6">
                        <form onSubmit={this.onSubmit}>
                            <h6>Search Form</h6>
                            <div className="form-group">
                                <label>x</label>
                                <input
                                    id='x'
                                    type="number"
                                    className="form-control"
                                    onChange={this.onChange}
                                    value={this.state.x}
                                    required
                                />
                            </div>
                            <div className="form-group">
                                <label>y</label>
                                <input
                                    id='y'
                                    type="number"
                                    className="form-control"
                                    onChange={this.onChange}
                                    value={this.state.y}
                                    required
                                />
                            </div>
                            <div className="form-group">
                                <label>n</label>
                                <input
                                    id='n'
                                    type="number"
                                    className="form-control"
                                    onChange={this.onChange}
                                    value={this.state.n}
                                    required
                                />
                            </div>

                            <div className="form-group">
                                <label>Operation Type</label>
                                <select
                                    id='operation_type'
                                    className="form-control"
                                    onChange={this.onChange}
                                    value={this.state.operation_type}
                                    required
                                >
                                    <option value='nearest'>nearest</option>
                                    <option value='furthest'>furthest</option>
                                </select>
                            </div>

                            <button type="submit" className="btn btn-primary btn-block">Search</button>
                        </form>

                    {this.state.search_history && this.state.search_history.length ?
                        <div className="history">
                            <p>Select inputs from available search history</p>
                            <table className="table table-hover">
                                <thead>
                                <tr>
                                    <th scope="col">x</th>
                                    <th scope="col">y</th>
                                    <th scope="col">n</th>
                                    <th scope="col">operation</th>
                                </tr>
                                </thead>
                                <tbody>
                                {this.state.search_history.map((point, index) => {
                                    return (
                                        <tr key={index} onClick={()=>this.handleAutoInput(point)}>
                                            <td>{point.x}</td>
                                            <td>{point.y}</td>
                                            <td>{point.n}</td>
                                            <td>{point.operation_type}</td>
                                        </tr>
                                    )

                                })}
                                </tbody>
                            </table>
                        </div>
                        :
                            <p>There is no search history</p>
                    }
                    </div>
                        {this.state.search_results && this.state.search_results.length ?
                            <div className=" col-sm-6 ">
                            <h6>Results for Points that
                                are {this.state.operation_type} to {this.state.x}, {this.state.y}</h6>
                            <table className="table">
                                <thead>
                                <tr>
                                    <th scope="col">id</th>
                                    <th scope="col">x</th>
                                    <th scope="col">y</th>
                                </tr>
                                </thead>
                                <tbody>
                                {this.state.search_results.map(point => {
                                    return (
                                        <tr>
                                        <th scope="row">{point.id}</th>
                                        <td>{point.point.coordinates[0]}</td>
                                        <td>{point.point.coordinates[1]}</td>
                                    </tr>
                                    )

                                })}
                                </tbody>
                            </table>
                        </div>
                        :
                        <br/>
                    }
                    </div>
                </div>
                :
                <div>
                    {this.props.history.push("/sign-in")}
                </div>

        );
    }
}

export default Home;