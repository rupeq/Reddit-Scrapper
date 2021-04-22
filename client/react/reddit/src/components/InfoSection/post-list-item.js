import React, {Component} from 'react';

import PostService from '../../service/index';


export default class PostListItem extends Component {
    postService = new PostService();

    constructor(props) {
        super(props);
        this.state = {
            posts: [],
            url:props.url,
            postsNumber:props.postsNumber
        }
    }

    componentDidMount() {
        console.log(this.state.url)
        this.postService.getPosts(this.state.url)
        .then((posts) => {
            this.setState({
                posts
            })
        })

        this.setState({
            postsNumber:this.state.posts.length
        })
    }

    componentDidUpdate(prevProps){
        if (this.props.url !== prevProps.url){
            this.updateList()
        }
    }

    updateList(prevProps){
        const {url} = this.props;
        if (!url){
            return;
        }

        this.postService.getPosts(url)
        .then((posts) => {
            this.setState({
                posts
            })
        })

        this.setState({
            postsNumber:this.state.posts.length
        })
    }


    render(){
        let posts = this.state.posts
        return(
            <div class="list-wrapper">
                {posts.map((post, index) => {
                    return(
                        <div key={post.uid} className="task-wrapper">
                            <span className="post-url">{post.post_url}; </span>
                            <span className="author">{post.author}; </span>
                            <span className="author-karma">{post.user_karma}; </span>
                            <span className="author-cake-day">{post.user_cake_day}; </span>
                            <span className="author-post-karma">{post.post_karma}; </span>
                            <span className="author-comment-karma">{post.user_comment_karma}; </span>
                            <span className="post-date">{post.post_date}; </span>
                            <span className="number-of-comments">{post.number_of_comments}; </span>
                            <span className="number-of-votes">{post.number_of_votes}; </span>
                            <span className="post-category">{post.post_category}; </span>
                        </div>
                    )
                })}
            </div>
        )
    }
}