import React from 'react';

import PostService from '../../service/index';

const Pagination = ({_, set}) => {
    const setPageNum = (num) => {
        set(`http://localhost:8080/posts/?page=${num}`)
    }


    const getPage = (postsNumber) => {
        let pages = []

        for (let i = 0; i<postsNumber; i++){
            pages.push(<input type="button"  onClick={e => {
                setPageNum(e.target.value)
            }} value={i}/>);
            pages.push(<br/>)
        }

        return pages
    }

    return(
        <div class="list-wrapper">
            {getPage(10)}
        </div>
    )
};

export default Pagination;