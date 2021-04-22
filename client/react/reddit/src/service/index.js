class PostService {
    async getResource(url) {
        const res = await fetch(url);

        if (!res.ok) {
            throw new Error(`Could not fetch ${url}, status ${res.status}`);
        }

        return await res.json();;
    };


    async getPosts(url){
        const posts = await this.getResource(url);
        return posts.map(this._transformPost);
    }

    _transformPost(posts) {
        return {
            uid: posts.uid,
            post_url: posts.post_url,
            author: posts.author,
            user_karma: posts.user_karma,
            user_cake_day: posts.user_cake_day,
            post_karma: posts.post_karma,
            user_comment_karma: posts.user_comment_karma,
            post_date: posts.post_date,
            number_of_comments: posts.number_of_comments,
            number_of_votes: posts.number_of_votes,
            post_category: posts.post_category,
        }
    }
}

export default PostService;