// middleware/auth.ts
import { useRuntimeConfig, useCookie, navigateTo } from "#imports";
import axios from "axios";
import { jwtDecode } from "jwt-decode";

export default defineNuxtRouteMiddleware(async (to) => {
  const token = <string>useCookie("auth_token").value;
  const config = useRuntimeConfig();
  const apiBase = config.public.apiBase as string;
  if (!token) {
    console.error("Токен отсутствует");
    return navigateTo("/");
  }

  try {
    const decodedToken = jwtDecode(token);
    const userId = decodedToken.user_id || null;

    const response = await axios.post(`${apiBase}/api/getUser`, {
      userId: userId,
    });

    const role = response.data.role;
    console.warn(role);
    if (role == 2) {
      return true;
    } else if (role == 1 || role == 0) {
      return navigateTo("/course");
    }
    return navigateTo("/");
  } catch (error) {
    console.error("Ошибка при декодировании токена:", error);
  }
});
