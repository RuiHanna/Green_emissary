gsap.registerPlugin(ScrollTrigger);
// 初始化定位
gsap.set([".parallax-layer"], {
    force3D: true  // 开启GPU加速
});

// 山脉层动画：缓慢下移
gsap.to("#mountain-layer", {
    y: "-70%",  // 向上移动露出更多山体
    scrollTrigger: {
        scrub: 1,
        start: "top top",
        end: "bottom bottom"
    }
});

//标题层
gsap.to("#title-layer", {
    y: "-20%",
    scale: 0.6,
    opacity: 0.1,
    scrollTrigger: {
        scrub: 1,
        start: "top top",
        end: "bottom bottom"
    }
})

// 设定初始位置（植物在底部隐藏）
gsap.set("#seedling", {y: "180%", opacity: 0});
gsap.set("#sapling", {x: "-40%", y: "180%", opacity: 0});
gsap.set("#tree", {x: "-55%", y: "180%", opacity: 0});

// 小草动画
gsap.timeline({
    scrollTrigger: {
        trigger: "#plant-container",
        start: "top 100%",  // 当页面滚动到触发点时
        end: "top -50%",    // 结束位置
        scrub: true,       // 滚动时动画平滑过渡
    }
})
    .to("#seedling", {y: "0%", opacity: 1, duration: 5})
    .to("#seedling", {opacity: 0, duration: 3}, "+=1");  // 停留后再消失

// 中树动画
gsap.timeline({
    scrollTrigger: {
        trigger: "#plant-container",
        start: "top 10%",
        end: "top -100%",
        scrub: true,
    }
})
    .to("#sapling", {x: "-40%", y: "-60%", opacity: 1, duration: 5})
    .to("#sapling", {opacity: 0, duration: 5}, "+=1");

// 大树动画
gsap.timeline({
    scrollTrigger: {
        trigger: "#plant-container",
        start: "top 10%",
        end: "top -150%",
        scrub: true,
    }
})
    .to("#tree", {x: "-55%", y: "-70%", opacity: 1, duration: 5});

gsap.registerPlugin(MotionPathPlugin);

// 太阳沿圆形轨迹上升
gsap.timeline({
    scrollTrigger: {
        trigger: "#sapling", // 以中树为触发点
        start: "top -30%",    // 当 #sapling 距离视口 80% 位置时触发
        end: "top -300%",      // 结束位置
        scrub: true
    }
})
    .to("#sun", {
        motionPath: {
            path: [
                {x: "0", y: "0"}, // 左下角开始
                {x: "100%", y: "-80%"}, // 最高点
                {x: "280%", y: "-170%"}  // 右下角
            ],
            curviness: 1.2,  // 让轨迹更平滑
        },
        duration: 3,
    });

// 文字淡入淡出
gsap.timeline({
    scrollTrigger: {
        trigger: "#sapling", // 让文字也在中树出现时触发
        start: "top -50%",
        end: "top -300%",
        scrub: true
    }
})
    .to("#text-container", {opacity: 1, duration: 1})

//太阳变大
gsap.timeline({
    scrollTrigger: {
        trigger: "#sapling", // 以中树为触发点
        start: "top -500%",    // 当 #sapling 距离视口 80% 位置时触发
        end: "top -550%",      // 结束位置
        scrub: true
    }
})
    .to("#sun", {
        x: "30%",
        y: "-120%",
        scale: 3,
        duration: 5,
    });


//背景大树长大
gsap.set("#big-tree", {opacity: 0.5})
gsap.timeline({
    scrollTrigger: {
        trigger: "sapling",
        start: "top -550%",
        end: "top -600%",
        scrub: true
    }
}).to("#big-tree", {
    y: "-100%",
    scale: 1.5,
    opacity: 1,
    duration: 2,
});
gsap.timeline({
    scrollTrigger: {
        trigger: "sapling",
        start: "top -600%",
        end: "top -650%",
        scrub: true
    }
}).to("#big-tree", {
    yPercent: -55,
});
gsap.timeline({
    scrollTrigger: {
        trigger: "sapling",
        start: "top -710%",
        end: "top -900%",
        scrub: true
    }
}).to("#big-tree", {
    yPercent: -220,
    ease: "none",
});
