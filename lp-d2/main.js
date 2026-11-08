// 追従ボタン：FVを過ぎたら出し、CTAのページと申込欄が見えている間は隠す
(function () {
  var btn = document.querySelector('.float');
  var top = document.getElementById('top');
  var hideAt = [document.getElementById('cta'), document.getElementById('apply')];
  if (!btn || !top || !('IntersectionObserver' in window)) return;
  var state = { top: true, cta: false, apply: false };
  function update() {
    var show = !state.top && !state.cta && !state.apply;
    btn.classList.toggle('show', show);
    btn.setAttribute('aria-hidden', show ? 'false' : 'true');
    btn.tabIndex = show ? 0 : -1;
  }
  new IntersectionObserver(function (e) { state.top = e[0].isIntersecting; update(); }).observe(top);
  new IntersectionObserver(function (e) { state.cta = e[0].isIntersecting; update(); }, { threshold: 0.25 }).observe(hideAt[0]);
  new IntersectionObserver(function (e) { state.apply = e[0].isIntersecting; update(); }).observe(hideAt[1]);
})();
