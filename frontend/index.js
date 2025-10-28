

const renderData = (data) => {
  const main = document.querySelector("main");
  data.reverse().forEach(async (obj) => {
    const div = document.createElement("div");
    div.className = "item-list";

    const imgDiv = document.createElement("div");
    imgDiv.className = "item-list__img";

    const infoDiv = document.createElement("div");
    infoDiv.className = "item-list__info";

    const img = document.createElement("img");
    const res = await fetch(`/images/${obj.id}`);
    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    img.src = url;

    const infoTitleDiv = document.createElement("div");
    infoTitleDiv.className = "item-list__info-title";
    infoTitleDiv.innerText = obj.title;

    const infoMetaDiv = document.createElement("div");
    infoMetaDiv.className = "item-list__info-meta";
    infoMetaDiv.innerText = obj.place + "ㆍ" + calcTime(obj.insertAt);

    const infoPriceDiv = document.createElement("div");
    infoPriceDiv.className = "item-list__info-price";
    infoPriceDiv.innerText = obj.price;

    imgDiv.appendChild(img);
    infoDiv.appendChild(infoTitleDiv);
    infoDiv.appendChild(infoMetaDiv);
    infoDiv.appendChild(infoPriceDiv);
    div.appendChild(imgDiv);
    div.appendChild(infoDiv);
    main.appendChild(div);
  });
};

const fetchList = async () => {
  // 로컬 저장소에서 저장된 토큰을 가져오는 방식 ------------------ (백엔드에서 쿠키를 http 응답 헤더에 담아 보내기 때문)
  // const accessToken = window.localStorage.getItem("token");
  // 로컬 저장소에서 저장된 토큰을 가져오는 방식 ------------------ (백엔드에서 쿠키를 http 응답 헤더에 담아 보내기 때문)

  const res = await fetch("/items", {
    // 인증 정보를 수동으로 호출하는 방식 ------------------ (백엔드에서 쿠키를 http 응답 헤더에 담아 보내기 때문)
    // headers: {
    //   Authorization: `Bearer ${accessToken}`,
    // },
    // 인증 정보를 수동으로 호출하는 방식 ------------------ (백엔드에서 쿠키를 http 응답 헤더에 담아 보내기 때문)
  });

  if (res.status === 401) {
    alert("로그인이 필요합니다.");
    window.location.pathname = "/login.html";
    return;
  }
  const data = await res.json();
  renderData(data);
};

fetchList();
