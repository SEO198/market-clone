const form = document.querySelector("#login-form");

const handleSubmit = async (event) => {
  event.preventDefault();
  const formData = new FormData(form);
  const sha256Password = sha256(formData.get("password"));
  formData.set("password", sha256Password);

  const res = await fetch("/login", {
    method: "POST",
    body: formData,
  });
  // 토큰을 쿠키에 저장 ----------------------------------- (백엔드에서 쿠키를 http 응답 헤더에 담아 보내기 때문)
  // const data = await res.json();
  // accessToken = data.access_token;
  // window.localStorage.setItem("token", accessToken);
  // 토큰을 쿠키에 저장 ----------------------------------- (백엔드에서 쿠키를 http 응답 헤더에 담아 보내기 때문)
  alert("로그인 되었습니다.");

  window.location.pathname = "/";
};

form.addEventListener("submit", handleSubmit);
