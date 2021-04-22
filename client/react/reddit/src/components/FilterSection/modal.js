import React from 'react';
import './modal.css';

import PostService from '../../service/index';

const Modal = ({active, setActive, _, setURL}) => {
    const activeModal = () => {
        setActive(false);
    }
    const setFilter = (filterType, filterVal) => {
        if (filterType == "all"){
            console.log(typeof setUrl)
            setURL(`http://localhost:8080/posts/`);
        }
        else{
            setURL(`http://localhost:8080/posts/?${filterType}=${filterVal}`);
        }
    }
    const setFilterType = (filterTypeValue) => {
        filterType = filterTypeValue;
    }
    const setFilterValue = (filterVal) => {
        setFilter(filterType, filterVal)
    }
    const submitFilter = () => {
        let filterValue = document.getElementById('filterValue').value;
        setFilterValue(filterValue);
    }

    let filterType = "";
    return (
        <div className={active ? 'modal active' : 'modal' }>
            <div className="popup-body">
                <div className="popup-content">
                    <h4>Filter by:</h4>
                    <select onChange={e => {
                        setFilterType(e.target.value)
                    }}>
                        <option value="all">All</option>
                        <option value="post_category">Post category</option>
                        <option value="post_date">Post date</option>
                        <option value="number_of_votes">Number of votes</option>
                    </select>
                    <input type="text" placeholder="value of filter" id="filterValue"/>
                    <input type="submit" value="Submit filter value" onClick={submitFilter} className="close-modal"/>
                    <input type="submit" value="Close" onClick={activeModal} className="close-modal"/>
                </div>
            </div>
        </div>
    );
};

export default Modal;