<div class="loading-background">
    <div>
        <i class="fas fa-cog fa-spin loading-icon"></i>
    </div>
</div>

<style lang="scss">
    .loading-background {
        width: 100vw;
        height: 100vh;
        background-color: rgba($color: #000000, $alpha: 0.8);
        display: flex;
        align-items: center;
        justify-content: center;
        position: fixed;
        left: 0;
        top: 0;
        z-index: 1000;
        
        .loading-icon {
            font-size: 200px;
            color: blue;
        }
    }
</style>