export const meta = {id: "VE-gsap-customease", plugin: "CustomEase", needs: ["gsap-customease"]};
export function register(gsap, libs) { gsap.registerPlugin(libs.CustomEase); }
export function registerEases(gsap, CustomEase) {
  gsap.registerPlugin(CustomEase);
  CustomEase.create("avsSoftOvershoot", "M0,0 C0.23,0 0.26,1.08 0.7,1.04 0.86,1.02 0.94,1 1,1");
  CustomEase.create("avsSnapSettle", "M0,0 C0.15,0 0.18,0.92 0.55,1 0.78,1.04 0.9,1 1,1");
  return {softOvershoot:"avsSoftOvershoot", snapSettle:"avsSnapSettle"};
}
