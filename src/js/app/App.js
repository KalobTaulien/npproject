import React, { useState, useEffect } from 'react';

// TODO:
// - [ ] Need a system of agreement to "vote" on others perspectives.

function agreementToEmoji(agreement) {
  /**
   * TODO: Move this to utils.js or something similar.
   * These `agreement` values match models.py/Comment.AGREEMENT_CHOICES
   * TODO:  Tooltips to help people understand what the emojis _actually_ mean would
   *        be helpful since :) can mean more than one thing in various cultures.
   */
  if (agreement == 4) {
    return "🤩";
  } else if (agreement == 2) {
    return "🙂";
  } else if (agreement == 0) {
    return "😐";
  } else if (agreement == -2) {
    return "😒";
  } else if (agreement == -4) {
    return "😡";
  }
}

function Reply(props) {
  const { reply } = props;
  return (
    <article className="prose my-5">
      <h4>Reply by {reply.user_name} feeling {agreementToEmoji(reply.agreement)}</h4>
      <p>{reply.reply}</p>
    </article>
  );
}

function ListReplies(props) {
  const { replies } = props;
  return (
    <div className="pl-10">
      {replies.map((reply, index) => (
        <Reply key={index} reply={reply} />
      ))}
    </div>
  );
}

function Comments(props) {
  const { userName, comment, replies} = props;
  return (
    <article className="prose">
      <h2>Comment by {userName} {agreementToEmoji(comment.agreement)}</h2>
      {comment.text}
      <ListReplies replies={replies} />
    </article>
  );
}


function App(props) {
    const [originalCommentData, setOriginalCommentData] = useState([]);

    useEffect(() => {
      fetch('http://localhost:8000/api/v1/comments/') // Versioned API URL
        .then(response => response.json())
        .then(data => {
          // Debating whether comments and replies should be separate or not. For now, I'm going with together.
          setOriginalCommentData(data)
        });
    }, []);

    return (
      <div>
        {originalCommentData && (
          <>
            {originalCommentData.map((comment, index) => (
              <Comments
                key={index}
                userName={comment.user_name}
                comment={comment}
                replies={comment.replies}
              />
            ))}
          </>
        )}
      </div>
    );
  }

  export default App;
