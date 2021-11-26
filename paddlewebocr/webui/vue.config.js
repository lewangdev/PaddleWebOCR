module.exports = {
  // publicPath :'/vue/'
  outputDir: '../dist',
  // productionSourceMap: true,
  configureWebpack: {
    devtool: 'source-map'
  },
  devServer: {
    proxy:{
      '/api':{
        target: 'http://localhost:8080',
        changeOrigin:true,
      }
    }

  },

}