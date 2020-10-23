from backend.models.post import Post
from backend.models.board import Board
from bson import ObjectId


class PostService:
    def delete_post(self, board_id, post_id):
        result = Post.objects(pk=post_id).delete()

        if not result:
            return False

        try:
            b = Board.objects.get(pk=board_id)
            Board.objects(pk=b.id).update_one(posts=list(
                filter(lambda p: p.id != ObjectId(post_id), b.posts)))

            return True
        except:
            return False

    def update(self, board_id, post_id, data) -> bool:
        try:
            post: Post = Post.objects.get(id=post_id)
            post.update(board_id=board_id,
                        title=data['title'], content=data['content'])
            if post.board_id != board_id:
                Board.exclude_post(post.board_id, post_id)
                Board.add_post(board_id, post)

            return True
        except:
            return False
