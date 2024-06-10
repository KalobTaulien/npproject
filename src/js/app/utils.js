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

export { agreementToEmoji };
