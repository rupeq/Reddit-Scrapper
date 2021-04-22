import React, { useEffect, useState } from "react";
import PostListItem from './post-list-item';

import Modal from '../FilterSection/modal';
import Pagination from '../PaginationSection/index';

const InfoSection = () => {
    const [modalActive, setActive] = useState(false);
    const [modalURL, setURL] = useState("http://localhost:8080/posts/");

    const active = () => setActive(true);
    return (
        <div className="app">
            <main>
                <input type="button" value="Filter" onClick={active}/>
                <Modal active={modalActive} setActive={setActive} setURL={setURL}/>
                <Pagination set={setURL} />
                <PostListItem url={modalURL}/>
            </main>
        </div>
    );
};

export default InfoSection;