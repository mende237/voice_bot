import React,{useState} from 'react'
import "./login.css";

export default function Register() {

    const [value, setValues] = useState({
        firstname :"",
        lastname  :"",
        password  :"",
        email     :"",
        cpassword :""
    }) ;

    const [submited, setSubmited] = useState(false);
    const [valid, setvalid] = useState(false);


      const handleFirstNameInputChange  =(event)=>{
        setValues({... value ,  firstname : event.target.value })
      }
      const handleLastNameInputChange  =(event)=>{
        setValues({...value, lastname : event.target.value })
      }
      const handleEmailInputChange = (event) => {
        setValues({ ...value, email: event.target.value })
    }
    const handlePasswordInputChange = (event) => {
        setValues({ ...value, password: event.target.value })
    }
    const handleCpasswordInputChange = (event) => {
        setValues({ ...value, cpassword: event.target.value })
    }

    const handleSubmit = (event) =>{
        event.preventDefault();
  
        if (value.email && value.firstName && value.lastName) {
            setvalid(true)
        }
        setSubmited(true);
      }

    return (
        <div class="container">

        <div class="card o-hidden border-0 shadow-lg my-5">
            <div class="card-body p-0">
                <div class="row">
                    <div class="background col-lg-5 d-none d-lg-block "></div>
                    <div class="col-lg-7">
                        <div class="p-5">
                            <div class="text-center">
                                <h1 class="h4 text-gray-900 mb-4">Create an Account!</h1>
                            </div>
                            <form class="user" onSubmit={handleSubmit}>
                                <div class="form-group row">
                                    <div class="col-sm-6 mb-3 mb-sm-0">
                                        <input type="text" class="form-control form-control-user" id="exampleFirstName"
                                            placeholder="First Name"
                                            value ={value.firstname}
                                            onChange ={handleFirstNameInputChange} />
                                           {submited && !value.firstName ?  <span style={{color:'red'}}> Please enter a last name</span> :null} 

                                    </div>
                                    <div class="col-sm-6">
                                        <input type="text" class="form-control form-control-user" id="exampleLastName"
                                            placeholder="Last Name" 
                                            value ={ value.lastname}
                                            onChange ={handleLastNameInputChange} />
                                                                   {submited && !value.lastName ?  <span style ={{color:'red'}}>Please enter a last name</span> :null} 
                                    </div>
                                </div>
                                <div class="form-group">
                                    <input type="email" class="form-control form-control-user" id="exampleInputEmail"
                                        placeholder="Email Address" 
                                        value={value.email} 
                                        onChange={handleEmailInputChange} />
                                       {submited && !value.email ?  <span style ={{color:'red'}}>Please enter a last name</span> :null} 

                                </div>
                                <div class="form-group row">
                                    <div class="col-sm-6 mb-3 mb-sm-0">
                                        <input type="password" class="form-control form-control-user"
                                            id="exampleInputPassword" placeholder="Password"
                                            value ={value.password} 
                                            onChange ={handlePasswordInputChange}/>
                                               {submited && !value.password ?  <span style ={{color:'red'}}>Please enter a password</span> :null} 
                                    </div>
                                    <div class="col-sm-6">
                                        <input type="password" class="form-control form-control-user"
                                            id="exampleRepeatPassword" placeholder="Repeat Password"
                                            value ={value.cpassword}
                                            onChange ={handleCpasswordInputChange} />
                                               {submited && !value.cpassword ?  <span style ={{color:'red'}}>Please enter confirmation password</span> :null} 
                                    </div>
                                </div>
                                <button className="btn btn-primary btn-user btn-block">  Register Account</button>
                                <hr/>
                                <a href="index.html" class="btn btn-google btn-user btn-block">
                                    <i class="fab fa-google fa-fw"></i> Register with Google
                                </a>
                                
                            </form>
                            <hr/>
                            <div class="text-center">
                                <a class="small" href="forgot-password.html">Forgot Password?</a>
                            </div>
                            <div class="text-center">
                                <a class="small" href="login.html">Already have an account? Login!</a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

    </div>

    )
}
