import React from 'react';
import '../../assets/css/style-min.css';

export default function Form() {
    return (
        <div className="container">
        <div className="card">
          <div className="card-header bg-primary">
            <h3 className="card-title text-white">Add caracterisque of paper</h3>
          </div>
          <div className="card-body">
            <div className="row">
              <div className="col-md-6">
                <div className="form-group">
                  <label>Minimal</label>
                  <select className="form-control select2" style={{width: "100%;"}}>
                    <option selected="selected">Alabama</option>
                    <option>Alaska</option>
                    <option>California</option>
                    <option>Delaware</option>
                    <option>Tennessee</option>
                    <option>Texas</option>
                    <option>Washington</option>
                  </select>
                </div>
                <div className="form-group">
                  <label>Disabled</label>
                  <select className="form-control select2" disabled="disabled" style={{wit: "100%"}}>
                    <option selected="selected">Alabama</option>
                    <option>Alaska</option>
                    <option>California</option>
                    <option>Delaware</option>
                    <option>Tennessee</option>
                    <option>Texas</option>
                    <option>Washington</option>
                  </select>
                </div>
              </div>
              <div className="col-md-6">
                <div className="form-group">
                  <label>Multiple</label>
                  <select className="select2" multiple="multiple" data-placeholder="Select a State" style={{width: "100%"}}>
                    <option>Alabama</option>
                    <option>Alaska</option>
                    <option>California</option>
                    <option>Delaware</option>
                    <option>Tennessee</option>
                    <option>Texas</option>
                    <option>Washington</option>
                  </select>
                </div>
                <div className="form-group">
                  <label>Disabled Result</label>
                  <select className="form-control select2" style={{width: "100%"}}>
                    <option selected="selected">Alabama</option>
                    <option>Alaska</option>
                    <option disabled="disabled">California (disabled)</option>
                    <option>Delaware</option>
                    <option>Tennessee</option>
                    <option>Texas</option>
                    <option>Washington</option>
                  </select>
                </div>
              </div>
            </div>

            <h5>Custom Color Variants</h5>
            <div className="row">
              <div className="col-12 col-sm-6">
                <div className="form-group">
                  <label>Minimal (.select2-danger)</label>
                  <select className="form-control select2 select2-danger" data-dropdown-css-className="select2-danger" style={{width: "100%"}}>
                    <option selected="selected">Alabama</option>
                    <option>Alaska</option>
                    <option>California</option>
                    <option>Delaware</option>
                    <option>Tennessee</option>
                    <option>Texas</option>
                    <option>Washington</option>
                  </select>
                </div>
              </div>              <div className="col-12 col-sm-6">
                <div className="form-group">
                  <label>Multiple (.select2-purple)</label>
                  <div className="select2-purple">
                    <select className="select2" multiple="multiple" data-placeholder="Select a State" data-dropdown-css-className="select2-purple" style={{width: "100%"}}>
                      <option>Alabama</option>
                      <option>Alaska</option>
                      <option>California</option>
                      <option>Delaware</option>
                      <option>Tennessee</option>
                      <option>Texas</option>
                      <option>Washington</option>
                    </select>
                  </div>
                </div>
              </div>
            </div>
          </div>
         
        </div>
        </div>
    )
}
