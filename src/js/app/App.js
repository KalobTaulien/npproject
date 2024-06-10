import React, { useState, useEffect } from 'react';


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
              <div>{comment.text} by {comment.user_name}</div>
            ))}
          </>
        )}
      </div>
    );
  }

  export default App;
