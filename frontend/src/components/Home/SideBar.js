import React,{useState} from 'react'
import './home.css';
import Login from "../Sigup/Login";
import Form from '../Form/Form';
import Register from '../Sigup/Register';


export default function SideBar() {

    const [value, setvalue] = useState(1);
    const [cat_val , setCat_val] = useState(false);
    

    return (
      <div id="page-top">

      <div id="wrapper">
            <ul className="navbar-nav bg-gradient-primary sidebar sidebar-dark accordion" id="accordionSidebar">
                <a className="sidebar-brand d-flex align-items-center justify-content-center" href="index.html">
                  <div className="sidebar-brand-icon rotate-n-15">
                      <i className="fas fa-laugh-wink"></i>
                  </div>
                  <div className="sidebar-brand-text mx-3">EasyInformation </div>
              </a>
  
              <hr className="sidebar-divider my-0"/>
  
              <li className="nav-item active m_nav-item" onClick = {()=>{setvalue(0)}}>
                  <a className="nav-link" href="#">
                      <i className="fas fa-fw fa-tachometer-alt"></i>
                      <span>View Tree </span></a>
              </li>

              <li className="nav-item active m_nav-item" onClick = {()=>{setvalue(1)}}>
                  <a className="nav-link" href="#">
                      <i className="fas fa-fw fa-tachometer-alt"></i>
                      <span>Construct Tree</span></a>
              </li>
              <li className="nav-item active m_nav-item" onClick = {()=>{setvalue(1)}}>
                  <a className="nav-link" href="#">
                      <i className="fas fa-fw fa-tachometer-alt"></i>
                      <span>Add other Admin</span></a>
              </li>
              <br />
              <hr className="sidebar-divider"/>
             

              <div className="sidebar-heading">
                  INTERFACE
              </div>
  
              <li className="nav-item m_nav-item" onClick = {()=>{setvalue(2)} }>
                  <a className="nav-link collapsed " href="#" data-toggle="collapse" data-target="#collapseTwo"
                      aria-expanded="true" aria-controls="collapseTwo">
                      <i className="fas fa-fw fa-cog"></i>
                      <span>Add Teachear</span>
                  </a>
              </li>
  
              <li className="nav-item">
                  <a className="nav-link collapsed m_nav-item " href="#" data-toggle="collapse" data-target="#collapseUtilities"
                      aria-expanded="true" aria-controls="collapseUtilities">
                      <i className="fas fa-fw fa-wrench"></i>
                      <span>Remove Teacher</span>
                  </a>
             </li>
             <li className="nav-item">
                  <a className="nav-link collapsed m_nav-item " href="#" data-toggle="collapse" data-target="#collapseUtilities"
                      aria-expanded="true" aria-controls="collapseUtilities">
                      <i className="fas fa-fw fa-wrench"></i>
                      <span>Set Category to Teacher</span>
                  </a>
             </li>
  
              <hr className="sidebar-divider"/>
  
          
              <hr className="sidebar-divider d-none d-md-block"/>
  
              <div className="text-center d-none d-md-inline">
                  <button className="rounded-circle border-0" id="sidebarToggle"></button>
              </div>
  
          </ul>
  
          <div id="content-wrapper" className="d-flex flex-column">
  
              <div id="content">
  
                  <nav className="navbar navbar-expand navbar-light bg-white topbar mb-4 static-top shadow">
  
                      <button id="sidebarToggleTop" className="btn btn-link d-md-none rounded-circle mr-3">
                          <i className="fa fa-bars"></i>
                      </button>
                        <form
                          className="d-none d-sm-inline-block form-inline mr-auto ml-md-3 my-2 my-md-0 mw-100 navbar-search">
                          <div className="input-group">
                              <input type="text" className="form-control bg-light border-0 small" placeholder="Search for..."
                                  aria-label="Search" aria-describedby="basic-addon2"/>
                              <div className="input-group-append">
                                  <button className="btn btn-primary" type="button">
                                      <i className="fas fa-search fa-sm"></i>
                                  </button>
                              </div>
                          </div>
                      </form>
                        <ul className="navbar-nav ml-auto">
                            <li className="nav-item dropdown no-arrow d-sm-none">
                              <a className="nav-link dropdown-toggle" href="#" id="searchDropdown" role="button"
                                  data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                  <i className="fas fa-search fa-fw"></i>
                              </a>
                              <div className="dropdown-menu dropdown-menu-right p-3 shadow animated--grow-in"
                                  aria-labelledby="searchDropdown">
                                  <form className="form-inline mr-auto w-100 navbar-search">
                                      <div className="input-group">
                                          <input type="text" className="form-control bg-light border-0 small"
                                              placeholder="Search for..." aria-label="Search"
                                              aria-describedby="basic-addon2"/>
                                          <div className="input-group-append">
                                              <button className="btn btn-primary" type="button">
                                                  <i className="fas fa-search fa-sm"></i>
                                              </button>
                                          </div>
                                      </div>
                                  </form>
                              </div>
                          </li>
  
                
  
                          <li className="nav-item dropdown no-arrow mx-1">
                              <a className="nav-link dropdown-toggle" href="#" id="messagesDropdown" role="button"
                                  data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                  <i className="fas fa-envelope fa-fw"></i>
                                 <div style={{display:'flex', justifyContent:'space-around'}}>
                                 <div style={{margin : '5%'}}>
                                  <button className="btn-primary rounded-pill"  >Login</button>
                                  </div>
                                      <div  style={{margin : '5%'}}>
                                      <button className="btn-primary rounded-pill" >SigNup</button>
                                      </div>
                                 </div>
                              </a>
                              <div className="dropdown-list dropdown-menu dropdown-menu-right shadow animated--grow-in"
                                  aria-labelledby="messagesDropdown">
                                  <h6 className="dropdown-header">
                                      Message Center
                                  </h6>
                                  <a className="dropdown-item d-flex align-items-center" href="#">
                                      <div className="dropdown-list-image mr-3">
                                          <img className="rounded-circle" src="img/undraw_profile_1.svg"
                                              alt="..."/>
                                          <div className="status-indicator bg-success"></div>
                                      </div>
                                      <div className="font-weight-bold">
                                          <div className="text-truncate">Hi there! I am wondering if you can help me with a
                                              problem I've been having.</div>
                                          <div className="small text-gray-500">Emily Fowler · 58m</div>
                                      </div>
                                  </a>
                                  <a className="dropdown-item d-flex align-items-center" href="#">
                                      <div className="dropdown-list-image mr-3">
                                          <img className="rounded-circle" src="img/undraw_profile_2.svg"
                                              alt="..."/>
                                          <div className="status-indicator"></div>
                                      </div>
                                      <div>
                                          <div className="text-truncate">I have the photos that you ordered last month, how
                                              would you like them sent to you?</div>
                                          <div className="small text-gray-500">Jae Chun · 1d</div>
                                      </div>
                                  </a>
                              </div>
                          </li>
  
                      </ul>
  
                  </nav>
  
                  <div className="container-fluid">
  
                      <div className="d-sm-flex align-items-center justify-content-between mb-4">
                          <h1 className="h3 mb-0 text-gray-800">Dashboard</h1>
                          <a href="#" className="d-none d-sm-inline-block btn btn-sm btn-primary shadow-sm"><i
                                  className="fas fa-download fa-sm text-white-50"></i> Generate Report</a>
                      </div>
  
                      <div className="row">
  
                         
                          <div className="col-xl-12 col-md-12 mb-4 " >
                              <div className="card border-left-primary shadow h-100 py-2">
                                  <div className="card-div">
                                        {value ==0 ? <div className="row"><Login></Login></div> :null }
                                        {value ==1 ? <div className="row"><Form></Form></div> :null }
                                        {value ==2 ? <div className="row"><Register></Register></div> :null }
                                  </div>
                              </div>
                          </div>
                      </div>
    
                      <div className="row">
  
                          <div className="col-xl-8 col-lg-7">
                              <div className="card shadow mb-4">
                                      <h6 className="m-0 font-weight-bold text-primary">Earnings Overview</h6>
                                  <div
                                      className="card-header py-3 d-flex flex-row align-items-center justify-content-between">
                                      <div className="dropdown no-arrow">
                                          <a className="dropdown-toggle" href="#" role="button" id="dropdownMenuLink"
                                              data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                              <i className="fas fa-ellipsis-v fa-sm fa-fw text-gray-400"></i>
                                          </a>
                                          <div className="dropdown-menu dropdown-menu-right shadow animated--fade-in"
                                              aria-labelledby="dropdownMenuLink">
                                              <div className="dropdown-header">Dropdown Header:</div>
                                              <a className="dropdown-item" href="#">Action</a>
                                              <a className="dropdown-item" href="#">Another action</a>
                                              <div className="dropdown-divider"></div>
                                              <a className="dropdown-item" href="#">Something else here</a>
                                          </div>
                                      </div>
                                  </div>
                                  <div className="card-div">
                                      <div className="chart-area">
                                          <canvas id="myAreaChart"></canvas>
                                      </div>
                                  </div>
                              </div>
                          </div>
  
                      
                      </div>
  
                  </div>
  
              </div>

              <footer className="sticky-footer bg-white">
                  <div className="container my-auto">
                      <div className="copyright text-center my-auto">
                          <span>Copyleft Ue Projet 2021-2022</span>
                      </div>
                  </div>
              </footer>
  
          </div>
  
      </div>
    
  </div>
      )
}
