const BundleTracker = require("webpack-bundle-tracker");

module.exports = {
  publicPath: "http://localhost:9000/static/common/dist/",
  productionSourceMap: false,
  pages: {
    app: "./js/main.js",
    cms: "./js/cms.js",
    'request-new-tenant': "./js/apps/workspace/entry-request-new-tenant",
    'list-requests': "./js/apps/workspace/entry-list-new-tenant-requests",
    'view-request': "./js/apps/workspace/entry-view-tenant-request",
    'admin-view-request': "./js/apps/custos_admin_portal_admin/entry-admin-view-tenant-request",
    'admin-edit-request': "./js/apps/custos_admin_portal_admin/entry-admin-edit-tenant-request",
    'admin-list-requests': "./js/apps/custos_admin_portal_admin/entry-admin-list-new-tenant-requests"
  },
  css: {
    loaderOptions: {
      postcss: {
        config: {
          path: __dirname
        }
      }
    }
  },
  configureWebpack: {
    plugins: [
      new BundleTracker({
        filename: "webpack-stats.json",
        path: "./dist/"
      })
    ],
    devtool: 'source-map',
    optimization: {
      /*
       * Force creating a vendor bundle so we can load the 'app' and 'vendor'
       * bundles on development as well as production using django-webpack-loader.
       * Otherwise there is no vendor bundle on development and we would need
       * some template logic to skip trying to load it.
       * See also: https://bitbucket.org/calidae/dejavu/src/d63d10b0030a951c3cafa6b574dad25b3bef3fe9/%7B%7Bcookiecutter.project_slug%7D%7D/frontend/vue.config.js?at=master&fileviewer=file-view-default#vue.config.js-27
       */
      splitChunks: {
        chunks: 'all',
        cacheGroups: {
          vendors: {
            name: 'chunk-vendors',
            test: /[\\/]node_modules[\\/]/,
            priority: -10,
            chunks: 'initial',
            reuseExistingChunk: true
          },
          common: {
            name: 'chunk-common',
            minChunks: 2,
            priority: -20,
            chunks: 'initial',
            reuseExistingChunk: true
          }
        }
      }
    },

  devServer: {
    port: 9000,
    headers: {
      "Access-Control-Allow-Origin": "*"
    },
    hot: true,
    hotOnly: true
  }
  }
};
