import React, { useState, useEffect } from 'react';



function Comments(props) {
  const { userName, comment } = props;
  return (
    <article className="prose">
      <h2>Comment by {userName}</h2>
      {comment.text}
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
              <Comments key={index} userName={comment.user_name} comment={comment} />
            ))}
          </>
        )}
      </div>
    );
  }

  export default App;
