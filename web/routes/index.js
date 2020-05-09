var express = require('express');
var router = express.Router();

/* GET home page. */
const indexFunc = function(req, res, next) {
  const problems = [1000, 1001, 1002, 1003, 1004];
  res.render('index', { title: 'Competitive Programming Tester', 'problems': problems });
};
router.get('/', indexFunc);
router.get('/:problem_name', indexFunc);

module.exports = router;
