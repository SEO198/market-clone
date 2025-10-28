<!-- <form id="login-form" action="/login" method="POST">
  <div>로그인 페이지</div>
  <div>
    <label for="id">아이디</label>
    <input type="text" id="id" name="id" required />
  </div>
  <div>
    <label for="password">패스워드</label>
    <input type="password" id="password" name="password" required />
  </div>
  <div>
    <button type="submit">로그인</button>
  </div>
  <div id="info"></div>
</form> -->
<script>
  import { getAuth, signInWithPopup, GoogleAuthProvider } from "firebase/auth";
  import { user$ } from "../store";

  const provider = new GoogleAuthProvider();
  const auth = getAuth();
  const loginWithGoogle = async () => {
    try {
      const result = await signInWithPopup(auth, provider);
      const credential = GoogleAuthProvider.credentialFromResult(result);
      const token = credential.accessToken;
      const user = result.user;
      user$.set(user);
      localStorage.setItem("token", token);
    } catch (error) {
      console.log(error);
    }
  };
</script>

<div>
  <!-- {#if $user$}
    <div>{$user$?.displayName} 로그인됨</div>
  {/if} -->
  <div>로그인 하기</div>
  <button class="login-btn" on:click={loginWithGoogle}>
    <div>
      <img
        class="google-logo"
        src="https://e7.pngegg.com/pngimages/734/947/png-clipart-google-logo-google-g-logo-icons-logos-emojis-tech-companies-thumbnail.png"
        alt=""
      />
    </div>
    <div>Google로 시작하기</div></button
  >
</div>

<style>
  .login-btn {
    width: 200px;
    height: 50px;
    border: 1px solid black;
    border-radius: 3px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .google-logo {
    width: 20px;
  }
</style>
