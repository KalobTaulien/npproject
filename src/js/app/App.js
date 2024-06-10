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

const ReplyForm = ({commentId, replies, originalCommentData, setOriginalCommentData}) => {
  /**
   * Using a destructed function based component to mix things up a bit (for peer reviews)
   */
  // Stays local to the Comment the Reply will be sent to.
  const [reply, setReply] = useState('');
  // To help direct users. Nothing is more frustrating than poor functionality with no user guidance :P
  const [errorMessage, setErrorMessage] = useState('');

  const handleChange = (event) => {
    setReply(event.target.value);
  };

  const handleSubmit = (event) => {
    // TODO: Disable the button to prevent multiple submissions, or better yet, add idempotency to the backend.
    event.preventDefault();

    // Unset the error message.
    setErrorMessage('');

    if(reply.length < 50) {
      setErrorMessage('Reply must be at least 50 characters long');
      return false;
    } else if(reply.length > 5000) {
      setErrorMessage('Reply must be less than 5000 characters long');
      return false;
    } else {
      // Basic frontend validation passed before hitting the backend.
      // Clean the error message while this is being submitted.
      setErrorMessage('');
    }

    fetch(`http://localhost:8000/api/v1/comments/${commentId}/`, {
      method: 'POST',
      headers: {
        'content-type': 'application/json',
      },
      body: JSON.stringify({
        reply: reply,
        comment_id: commentId,
      })
    })
    .then(response => {
      if (!response.ok) { // Checks if the response status code is not in the 200..ish range
        return response.json().then(err => {
          // Throws the error JSON which can be caught in the catch block
          // Then we can display that error.
          throw err;
        });
      }

      // Only parse JSON if response is ok
      return response.json();
    })
    .then(newReply => {
      setReply('');
      // Update the entire comment and data structure with the new reply.
      setOriginalCommentData(originalCommentData => originalCommentData.map(comment => {
        if (comment.id === commentId) {
          return {
            ...comment,
            replies: [...comment.replies, newReply]
          };
        }
        return comment;
      }));
    })
    .catch((error) => {
      // Set the error message
      setErrorMessage(error)
    });
  }


  return (
    // The styling is 100% from Tailwind UI. What a beautiful time saver that library is <3
    <form onSubmit={handleSubmit}>
      <label htmlFor="comment" className="block text-sm font-medium leading-6 text-gray-900">Add your reply</label>
      <div className="mt-2">
        {/* TODO: Apply autoexpanding Textarea to signal that users long form conversations are welcomed. */}
        <textarea rows="4" name="comment" id="comment" required="required" minLength={50} maxLength={5000}className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6" onChange={handleChange} value={reply}></textarea>
      </div>
      <div className="mt-4">
        {errorMessage && <div className="text-red-500 text-sm my-4">{errorMessage}</div>}
        <button type="submit" className="inline-flex items-center rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">Reply</button>
      </div>
    </form>
  )
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
  const { replies, commentId, originalCommentData, setOriginalCommentData } = props;
  return (
    <div className="pl-10">
      {replies.map((reply, index) => (
        <Reply key={index} reply={reply} />
      ))}

      <ReplyForm
        commentId={commentId}
        replies={replies}
        originalCommentData={originalCommentData}
        setOriginalCommentData={setOriginalCommentData}
      />
    </div>
  );
}


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
                setOriginalCommentData={setOriginalCommentData}
                originalCommentData={originalCommentData}
              />
            ))}
          </>
        )}
      </div>
    );
  }

  export default App;
