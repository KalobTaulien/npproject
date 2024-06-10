import React from 'react';

import { agreementToEmoji } from '../utils';
import { ListReplies } from './Replies';


function Comments(props) {
    const { userName, comment, replies, originalCommentData, setOriginalCommentData } = props;
    return (
      <article className="prose">
        <h2>Comment by {userName} {agreementToEmoji(comment.agreement)}</h2>
        {comment.text}
        <ListReplies
          replies={replies}
          commentId={comment.id}
          originalCommentData={originalCommentData}
          setOriginalCommentData={setOriginalCommentData}
        />
      </article>
    );
}

export default Comments;
