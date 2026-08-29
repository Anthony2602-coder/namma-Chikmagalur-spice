(function () {
    const APK_PATHS = [
        '/static/namma-chikmagaluru.apk',
        '/release-assets/namma-chikmagaluru.apk',
        '/namma-chikmagaluru.apk'
    ];
    const btn = document.getElementById('downloadBtn');
    const status = document.getElementById('status');
    const directLink = document.getElementById('directLink');
    let apkUrl = null;

    async function findApk() {
        for (const path of APK_PATHS) {
            try {
                const res = await fetch(path, { method: 'HEAD' });
                if (res.ok) {
                    apkUrl = path;
                    directLink.href = path;
                    directLink.textContent = 'Direct: ' + path;
                    status.textContent = 'APK ready for download';
                    status.style.color = '#27ae60';
                    return;
                }
            } catch (e) { /* try next */ }
        }
        status.textContent = 'APK not built yet. Run GitHub Actions "Build Android APK" workflow or build locally.';
        status.style.color = '#c8952e';
        btn.disabled = true;
        btn.style.opacity = '0.6';
    }

    btn.addEventListener('click', () => {
        if (apkUrl) {
            const a = document.createElement('a');
            a.href = apkUrl;
            a.download = 'namma-chikmagaluru.apk';
            document.body.appendChild(a);
            a.click();
            a.remove();
            status.textContent = 'Download started! Open the APK from Downloads to install.';
        }
    });

    findApk();
})();
