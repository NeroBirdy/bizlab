// middleware/auth.ts
import { useRuntimeConfig, useCookie, navigateTo } from "#imports";
import axios from "axios";
import { jwtDecode } from "jwt-decode";

interface TokenRefreshResponse {
  access: string;
  refresh: string;
}

export default defineNuxtRouteMiddleware(async (to) => {
  if (["/auth/login", "/auth/register"].includes(to.path)) {
    return;
  }

  const {
    public: { apiBase },
  } = useRuntimeConfig();
  const userStore = useAuthStore();
  const authCookie = useCookie<string | null>("auth_token");
  const refreshCookie = useCookie<string | null>("refresh_token");
  if (!userStore.isAuth) {
    authCookie.value = null;
    refreshCookie.value = null;
    return redirectToMain();
  }

  if (!authCookie.value && !refreshCookie.value) {
    userStore.logoutUser();
    return redirectToMain();
  }

  try {
    await $fetch(`${apiBase}/api/token/verify/`, {
      method: "POST",
      body: { token: authCookie.value },
    });
    return isAuth();
  } catch {
    try {
      const response = await $fetch<TokenRefreshResponse>(
        `${apiBase}/api/token/refresh/`,
        {
          method: "POST",
          body: { refresh: refreshCookie.value },
        }
      );
      authCookie.value = response.access;
      isAuth();
    } catch {
      authCookie.value = null;
      refreshCookie.value = null;
      userStore.logoutUser();
      return redirectToMain();
    }
  }

  function redirectToMain() {
    if (to.path !== "/") {
      return navigateTo("/", { external: true });
    }
  }

  async function isAuth() {
    const decodedToken = jwtDecode(authCookie.value!);
    const userId = decodedToken.user_id || null;

    var temp_arr = to.path.split("/");

    if (temp_arr[1] == "course" && temp_arr.length == 3) {
      if (!isPositiveInteger(temp_arr[2])) {
        return false;
      }
      try {
        const response = await $fetch(`${apiBase}/api/accessForCourse`, {
          method: "POST",
          body: { userId: userId, courseId: temp_arr[2] },
        });
        if (response) {
          if (!userStore.isAuth) {
            userStore.loginUser();
          }
          return true;
        } else return false;
      } catch (e) {
        console.error(e);
        return false;
      }
    } else if (temp_arr[1] == "courseForStudent" && temp_arr.length == 3) {
      if (!isPositiveInteger(temp_arr[2])) {
        return false;
      }
      try {
        const response = await $fetch(
          `${apiBase}/api/accessForCourseForStudent`,
          {
            method: "POST",
            body: { userId: userId, courseId: temp_arr[2] },
          }
        );
        if (response) {
          if (!userStore.isAuth) {
            userStore.loginUser();
          }
          return true;
        } else return false;
      } catch (e) {
        console.error(e);
        return false;
      }
    } else if (temp_arr[1] == "test" && temp_arr.length == 3) {
      if (!isPositiveInteger(temp_arr[2])) {
        return false;
      }
      try {
        const response = await $fetch(`${apiBase}/api/accessForTest`, {
          method: "POST",
          body: { userId: userId, materialId: temp_arr[2] },
        });
        if (response) {
          if (!userStore.isAuth) {
            userStore.loginUser();
          }
          return true;
        } else return false;
      } catch (e) {
        console.error(e);
        return false;
      }
    } else {
      if (!userStore.isAuth) {
        userStore.loginUser();
      }
    }
  }

  function isPositiveInteger(str) {
    const regex = /^\d+$/;
    return regex.test(str);
  }
});
