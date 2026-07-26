import { type RouteConfig, index, route } from "@react-router/dev/routes";

export default [
  index("routes/home.tsx"),
  route("araclar/birlestir", "routes/araclar.birlestir.tsx"),
  route("araclar/bol", "routes/araclar.bol.tsx"),
  route("araclar/sikistir", "routes/araclar.sikistir.tsx"),
] satisfies RouteConfig;
