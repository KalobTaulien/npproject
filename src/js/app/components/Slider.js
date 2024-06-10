import React, { useState } from 'react';
import { agreementToEmoji } from '../utils';

const Slider = ({ moodValue, setMoodValue} ) => {
    const [moodDisplay, setMoodDisplay] = useState("😐");

    function handleChange(e) {
      const val = e.target.value;
      setMoodValue(val);
      setMoodDisplay(agreementToEmoji(val));
    }

    return (
      <div className="inline-flex text-xl">
        <input type="range" value={moodValue} step="2" min="-4" max="4" onChange={handleChange} />
        <p className="text-2xl">{moodDisplay}</p>
      </div>
    );
}

export default Slider;
