/** @format */

// Components
// FIXME (of ud-viz package ?): in order to import itowns one must import
// the Game module that eslint complains as not being used
import { Widgets, Components, Game } from 'ud-viz';
import * as itowns from 'itowns';
import * as THREE from 'three';
import { CSS3DObject, CSS3DRenderer } from 'three-css3drenderer';
import proj4 from 'proj4';
import './BaseDemo.css';
import { BillBoard } from './Billboard';

const jquery = require('jquery');

const { ModuleView } = Components;
const { TilesManager } = Components;
const { LayerManager } = Components;
const { $3DTemporalBatchTable } = Widgets;
const { $3DTemporalBoundingVolume } = Widgets;
const { $3DTemporalTileset } = Widgets;

/**
* Represents the base HTML content of a demo for UD-Viz and provides methods to
* dynamically add module views.
*/
export class BaseDemo {
  constructor() {
    this.modules = {};
    this.moduleNames = {};
    this.moduleActivation = {};
    this.moduleBindings = {};
    this.requireAuthModules = [];
    this.authService = undefined;
    this.config = {};
    this.parentElement = undefined;
    this.view = undefined; // itowns view (3d scene)
    this.extent = undefined; // itowns extent (city limits)
    this.controls = undefined;
    /**
     * Object used to manage all of the layer.
     *
     * @type {LayerManager}
     */
    this.layerManager = undefined;
  }

  start(path) {
    const _this = this;
    this.appendTo(document.body);
    this.loadConfigFile(path).then(() => {
      this.reconfigureConfigurationUrls();
      // Use the stable server
      _this.addLogos();

      // Initialize iTowns 3D view
      _this.init3DView();
      _this.addBaseMapLayer();
      _this.addElevationLayer();
      _this.setupAndAdd3DTilesLayer();
      _this.update3DView();

      // //// REQUEST SERVICE
      const requestService = new Components.RequestService();

      // //// AUTHENTICATION MODULE
      if (_this.config.widgets.authenticationView) {
        const authenticationService = new Widgets.Extensions.AuthenticationService(
          requestService,
          _this.config,
        );
        const authenticationView = new Widgets.Extensions.AuthenticationView(
          authenticationService,
        );
        _this.addModuleView('authentication', authenticationView, {
          type: BaseDemo.AUTHENTICATION_MODULE,
        });
      }

      // //// DOCUMENTS MODULE
      let documentModule = null;
      if (_this.config.widgets.documentModule) {
        documentModule = new Widgets.DocumentModule(
          requestService,
          _this.config,
        );
        _this.addModuleView('documents', documentModule.view);

        // //// DOCUMENTS VISUALIZER (to orient the document)
        if (_this.config.widgets.documentVisualizerWindow) {
          const imageOrienter = new Widgets.DocumentVisualizerWindow(
            documentModule,
            _this.view,
            _this.controls,
          );

          // //// CONTRIBUTE EXTENSION
          if (_this.config.widgets.contributeModule) {
            const contribute = new Widgets.Extensions.ContributeModule(
              documentModule,
              imageOrienter,
              requestService,
              _this.view,
              _this.controls,
              _this.config,
            );
          }
        }

        // //// VALIDATION EXTENSION
        if (_this.config.widgets.documentValidationModule) {
          const validation = new Widgets.Extensions.DocumentValidationModule(
            documentModule,
            requestService,
            _this.config,
          );
        }

        // //// DOCUMENT COMMENTS
        if (_this.config.widgets.documentCommentsModule) {
          const documentComments = new Widgets.Extensions.DocumentCommentsModule(
            documentModule,
            requestService,
            _this.config,
          );
        }

        // //// GUIDED TOURS MODULE
        if (_this.config.widgets.guidedTourController) {
          const guidedtour = new Widgets.GuidedTourController(
            documentModule,
            requestService,
            _this.config,
          );
          _this.addModuleView('guidedTour', guidedtour, {
            name: 'Guided Tours',
          });
        }

        // //// CAMERA POSITIONER
        if (_this.config.widgets.cameraPositionerView) {
          const cameraPosition = new Widgets.CameraPositionerView(
            _this.view,
            _this.controls,
          );
          _this.addModuleView('cameraPositioner', cameraPosition);
        }

        // //// BillBoard
        /*const billboard = new BillBoard();

        // Chimney
        const sprite = billboard.CreateBillBoard('./assets/img/web_Source0.jpg', new THREE.Vector3(1843419.7372375734, 5164761.581669409, 275.0925693228869),
          new THREE.Vector3(240, 190, 1.0));
        sprite.updateMatrixWorld();
        this.view.scene.add(sprite);

        */
        // CSS3D----------------------------------------------------------------
        var scene2, renderer2;

        scene2 = new THREE.Scene();

        // create the iframe to contain webpage
        let planeWidth = 360;
        let planeHeight = 200;
        let element	= document.createElement('iframe');
        // webpage to be loaded into iframe
        //element.src	= "src/Helpers/mapage.html";
        element.src	= "http://rict2.liris.cnrs.fr/UD-Viz/UD-Viz-Core/examples/DemoFull/Demo.html";
        // width of iframe in pixels
        let elementWidth = 1280;
        // force iframe to have same relative dimensions as planeGeometry
        let aspectRatio = planeHeight / planeWidth;
        let elementHeight = elementWidth * aspectRatio;
        element.style.width  = elementWidth + "px";
        element.style.height = elementHeight + "px";

        let domObject = new CSS3DObject( element );
        domObject.position.x = 1843419.7372375734;
        domObject.position.y = 5164761.581669409;
        domObject.position.z = 275.0925693228869;
        domObject.rotation.x = -4.7;
        domObject.rotation.y = 0;
        domObject.rotation.z = 0;
        //scene2.add( domObject );


        // Second iframe
        let planeWidth2 = 360;
        let planeHeight2 = 200;
        let element2	= document.createElement('iframe');
        // webpage to be loaded into iframe
        //element.src	= "src/Helpers/mapage.html";
        element2.src	= "src/Helpers/VIDEO360 IFPEN Lyon.mp4";
        // width of iframe in pixels
        let elementWidth2 = 1280;
        // force iframe to have same relative dimensions as planeGeometry
        let aspectRatio2 = planeHeight2 / planeWidth2;
        let elementHeight2 = elementWidth2 * aspectRatio2;
        element2.style.width  = elementWidth2 + "px";
        element2.style.height = elementHeight2 + "px";

        let domObject2 = new CSS3DObject( element2 );
        domObject2.position.x = 1840600.6829996328;
        domObject2.position.y = 5167231.67695955;
        domObject2.position.z = 733.8620692362946;
        domObject2.rotation.x = -4.7;
        domObject2.rotation.y = 0;
        domObject2.rotation.z = 0;
        scene2.add( domObject2 );

        //CSS3DRenderer
        renderer2 = new CSS3DRenderer();
        renderer2.setSize( window.innerWidth, window.innerHeight );
        renderer2.domElement.style.position = 'absolute';
        renderer2.domElement.style.top = 0;
        renderer2.domElement.style.zIndex = 2;
        renderer2.domElement.id = "CSS3DRenderer";
        this.viewerDivElement.appendChild( renderer2.domElement );

        const camera = this.view.camera.camera3D;
        const tick = function(){
          requestAnimationFrame(tick)
          renderer2.render(scene2,camera)
          }
        tick()
      }
    });
  }

  /**
   * Reconfigure the url requiring it. Such dynamic reconfigurations allows
   * the definition of server independent deployments.
   */
  reconfigureConfigurationUrls() {
    // FIXME Although this regroups the code sharing the same concern
    // it should also repeat the tests for the existence of those properties...
    this.config['3DTilesLayer'].url = BaseDemo.ReconfigureUrlWithPort(
      this.config['3DTilesLayer'].url,
    );
    this.config.server.url = BaseDemo.ReconfigureUrlWithoutPort(
      this.config.server.url,
    );
  }

  /**
   * Returns the basic html content of the demo
   */
  get html() {
    return /* html */ `
           <header id="${this.headerId}">
               <div>
                   <h1>Derrière les fumées</h1>
                   <div id="${this.authFrameLocationId}"></div>
               </div>
               <div id="_base_demo_struct_header_panel">
                   <p style="display: inline-block; color: white; margin: 0;">
                       Icons made by <a href="https://www.freepik.com/"
                       title="Freepik">Freepik</a> from
                       <a href="https://www.flaticon.com/"
                       title="Flaticon">www.flaticon.com</a><br> is licensed by
                       <a href="http://creativecommons.org/licenses/by/3.0/"
                       title="Creative Commons BY 3.0" target="_blank">
                       CC 3.0 BY</a>
                   </p>
               </div>
           </header>
           <div id="_base_demo_stuct_main_panel">
               <nav>
                   <ul id="${this.menuId}">
                   </ul>
               </nav>
               <section id="${this.contentSectionId}">
                   <div id="${this.viewerDivId}"></div>
               </section>
           </div>
       `;
  }

  addLogos() {
    const { logos } = this.config.assets;
    const { imageFolder } = this.config.assets;

    for (let i = 0; i < logos.length; i += 1) {
      const img = document.createElement('img');
      img.src = imageFolder.concat('/'.concat(logos[i]));
      img.classList.add('logos');
      const src = document.getElementById('_base_demo_struct_header_panel');
      src.appendChild(img);
    }
  }

  /**
   * Returns the html element representing the upper-left frame of the UI,
   * which contains informations
   * about the logged in user.
   */
  get authenticationFrameHtml() {
    return /* html */ `
           <div id="${this.authenticationMenuLoggedInId}">
               <div id="${this.authenticationUserNameId}"></div>
               <button type="button" id="${this.authenticationLogoutButtonId}"
               class="logInOut">Logout</button>
           </div>
           <div id="${this.authenticationMenuLoggedOutId}">
               <button type="button" id="${this.authenticationLoginButtonId}"
               class="logInOut">Sign in</button>
           </div>
       `;
  }

  /**
   * Appends the demo HTML to an HTML element.
   *
   * @param htmlElement The parent node to add the demo into. The
   * recommended way of implementing the demo is simply to have an
   * empty body and call this method with `document.body` as
   * parameter.
   */
  appendTo(htmlElement) {
    this.parentElement = htmlElement;
    const div = document.createElement('div');
    div.innerHTML = this.html;
    div.id = this.mainDivId;
    htmlElement.appendChild(div);
  }

  // ////// MODULE MANAGEMENT

  /**
   * Adds a new module view to the demo.
   *
   * @param moduleId A unique id. Must be a string without spaces. It
   * will be used to generate some HTML ids in the page. It will also
   * be used to look for an icon to put with the button
   * @param moduleClass The module view class. Must implement some
   * methods (`enable`, `disable` and `addEventListener`). The
   * recommended way of implementing them is to extend the
   * `ModuleView` class, as explained [on the
   * wiki](https://github.com/MEPP-team/UD-Viz/wiki/Generic-demo-and-modules-with-ModuleView-&-BaseDemo).
   * @param options An object used to specify various options.
   * `options.name` allows you to specify the name that will be
   * displayed in the toggle button. By default, it makes a
   * transformation of the id (like this : myModule -> My Module).
   * `options.type` is the "type" of the module view that defines how
   * it is added to the demo. The default value is `MODULE_VIEW`,
   * which simply adds a toggle button to the side menu. If set to
   * `AUTHENTICATION_MODULE`, an authentication frame will be created
   * in the upper left corner of the page to contain informations
   * about the user. `options.requireAuth` allows you to
   * specify if this module can be shown without authentication (ie.
   * if no user is logged in). The default value is `false`. If set to
   * `true`, and no athentication module was loaded, it has no effect
   * (the module view will be shown). `options.binding` is the shortcut
   * key code to toggle the module. By default, no shortcut is created.
   */
  addModuleView(moduleId, moduleClass, options = {}) {
    if (
      typeof moduleClass.enable !== 'function'
      || typeof moduleClass.disable !== 'function'
    ) {
      throw new Error('A module must implement at least an enable()'
                    + 'and a disable() methods');
    }

    // Default name is the id transformed this way :
    // myModule -> My Module
    // my_module -> My module
    let moduleName = moduleId
      .replace(/([A-Z])/g, ' $1')
      .replace(/_/g, ' ')
      .replace(/^./, (str) => str.toUpperCase());
    let type = BaseDemo.MODULE_VIEW;
    let requireAuth = false;
    if (!!options) {
      if (!!options.type) {
        if (
          options.type === BaseDemo.MODULE_VIEW
          || options.type === BaseDemo.AUTHENTICATION_MODULE
        ) {
          type = options.type;
        } else {
          throw new Error(`Invalid value for option 'type': '${options.type}'`);
        }
      }
      if (!!options.name) {
        moduleName = options.name;
      }
      if (!!options.requireAuth) {
        requireAuth = options.requireAuth;
      }
    }
    const { binding } = options;

    this.modules[moduleId] = moduleClass;
    this.moduleNames[moduleName] = moduleId;
    this.moduleActivation[moduleId] = false;

    moduleClass.addEventListener(ModuleView.EVENT_ENABLED, () => {
      this.moduleActivation[moduleId] = true;
    });
    moduleClass.addEventListener(ModuleView.EVENT_DISABLED, () => {
      this.moduleActivation[moduleId] = false;
    });

    switch (type) {
      case BaseDemo.MODULE_VIEW:
        // create a new button in the menu
        this.createMenuButton(moduleId, moduleName, binding);
        break;
      case BaseDemo.AUTHENTICATION_MODULE:
        this.createAuthenticationFrame(moduleId);
        break;
      default:
        throw new Error(`Unknown module type : ${type}`);
    }

    if (requireAuth) {
      this.requireAuthModules.push(moduleId);
      this.updateAuthentication();
    }

    if (!!binding) {
      this.moduleBindings[binding] = moduleId;
    }
  }

  /**
   * Creates a new button in the side menu.
   * @param moduleId The module id.
   * @param buttonText The text to display in the button.
   * @param {String} [accessKey] The key binding for the module.
   */
  createMenuButton(moduleId, buttonText, accessKey) {
    const button = document.createElement('li');
    button.id = this.getModuleButtonId(moduleId);
    button.innerHTML = `<p class="_base_demo_menu_hint">${buttonText}</p>`;
    if (!!accessKey) {
      button.accessKey = accessKey;
    }
    this.menuElement.appendChild(button);
    const icon = document.createElement('img');

    // creating an icon
    icon.setAttribute(
      'src',
      `${this.config.assets.iconFolder}/${moduleId}.svg`
    );
    icon.className = 'menuIcon';
    button.insertBefore(icon, button.firstChild);

    // define button behavior
    button.onclick = (() => {
      this.toggleModule(moduleId);
    }).bind(this);
    const moduleClass = this.getModuleById(moduleId);

    // dynamically color the button
    moduleClass.parentElement = this.viewerDivElement.parentElement;
    moduleClass.addEventListener(ModuleView.EVENT_ENABLED, () => {
      button.className = 'choiceMenu choiceMenuSelected';
    });
    moduleClass.addEventListener(ModuleView.EVENT_DISABLED, () => {
      button.className = 'choiceMenu';
    });
    moduleClass.disable();
  }

  /**
   * Creates an authentication frame for the authentication module.
   * @param authModuleId The id of the authentication module.
   */
  createAuthenticationFrame(authModuleId) {
    const frame = document.createElement('div');
    frame.id = this.authenticationFrameId;
    frame.innerHTML = this.authenticationFrameHtml;
    this.authFrameLocationElement.appendChild(frame);
    const authView = this.getModuleById(authModuleId);
    authView.parentElement = this.viewerDivElement.parentElement;
    const authService = authView.authenticationService;
    this.authenticationLoginButtonElement.onclick = () => {
      if (this.isModuleActive(authModuleId)) {
        authView.disable();
      } else {
        authView.enable();
      }
    };
    this.authenticationLogoutButtonElement.onclick = () => {
      try {
        authService.logout();
      } catch (e) {
        console.error(e);
      }
    };

    authService.addObserver(this.updateAuthentication.bind(this));
    this.authService = authService;
    this.updateAuthentication();
  }

  /**
   * This method should be called when the authentication state changes
   *  (ie. a user log in / out), or when a module is added. It has two
   *  purposes :
   *  1. To update the upper-left square of the side menu (which contains
   *     use informations)
   *  2. To show / hide the modules that require authentication (as defined
   *     by the `options` parameter in the method `addModuleView`
   */
  updateAuthentication() {
    if (!!this.authService) {
      if (this.authService.isUserLoggedIn()) {
        const user = this.authService.getUser();
        this.authenticationMenuLoggedInElement.hidden = false;
        this.authenticationMenuLoggedOutElement.hidden = true;
        this.authenticationUserNameElement.innerHTML = `Logged in as <em>${user.firstname} ${user.lastname}</em>`;
        for (let mid of this.requireAuthModules) {
          this.getModuleButton(mid).style.removeProperty('display');
        }
      } else {
        this.authenticationMenuLoggedInElement.hidden = true;
        this.authenticationMenuLoggedOutElement.hidden = false;
        for (let mid of this.requireAuthModules) {
          this.getModuleButton(mid).style.setProperty('display', 'none');
        }
      }
    }
  }

  /**
   * Returns if the module view is currently enabled or not.
   * @param moduleId The module id.
   */
  isModuleActive(moduleId) {
    return this.moduleActivation[moduleId];
  }

  /**
   * Returns the module view class by its id.
   * @param moduleId The module id.
   */
  getModuleById(moduleId) {
    return this.modules[moduleId];
  }

  /**
   * If the module view is enabled, disables it, else, enables it.
   * @param moduleId The module id.
   */
  toggleModule(moduleId) {
    if (!this.isModuleActive(moduleId)) {
      this.getModuleById(moduleId).enable();
    } else {
      this.getModuleById(moduleId).disable();
    }
  }

  getModuleButtonId(moduleId) {
    return `_base_demo_menu_button${moduleId}`;
  }

  // Get module button element
  getModuleButton(moduleId) {
    return document.getElementById(this.getModuleButtonId(moduleId));
  }

  /**
   * Adds WMS elevation Layer of Lyon in 2012 and WMS imagery layer of Lyon
   * in 2009 (from Grand Lyon data).
   */
  addBaseMapLayer() {
    const wmsImagerySource = new itowns.WMSSource({
      extent: this.extent,
      name: this.config['background_image_layer']['name'],
      url: this.config['background_image_layer']['url'],
      version: this.config['background_image_layer']['version'],
      projection: this.config['projection'],
      format: this.config['background_image_layer']['format'],
    });
    // Add a WMS imagery layer
    let wmsImageryLayer = new itowns.ColorLayer(
      this.config['background_image_layer']['layer_name'],
      {
        updateStrategy: {
          type: itowns.STRATEGY_DICHOTOMY,
          options: {},
        },
        source: wmsImagerySource,
        transparent: true,
      },
    );
    this.view.addLayer(wmsImageryLayer);
  }

  addElevationLayer() {
    // Add a WMS elevation source
    const wmsElevationSource = new itowns.WMSSource({
      extent: this.extent,
      url: this.config['elevation_layer']['url'],
      name: this.config['elevation_layer']['name'],
      projection: this.config['projection'],
      heightMapWidth: 256,
      format: this.config['elevation_layer']['format'],
    });
    // Add a WMS elevation layer
    const wmsElevationLayer = new itowns.ElevationLayer(
      this.config['elevation_layer']['layer_name'],
      {
        useColorTextureElevation: true,
        colorTextureElevationMinZ: 144,
        colorTextureElevationMaxZ: 622,
        source: wmsElevationSource,
      },
    );
    this.view.addLayer(wmsElevationLayer);
  }

  /**
   * The configuration file of demo defines URL of resources. At the time
   * of the writing of the configuration of the demo the Fully Qualified Domain 
   * Name (FQDN) of the server hosting the demo is not yet known (and will
   * only be known at deployment time). It is thus configured with the 
   * 'DEMO_SERVER' keyword (in the configuration file) that is replaced (at 
   * run time) through the usage of this function.
   * This version (as opposed to ReconfigureUrlWithPort) does NOT include
   * the port number.
   * @param  {string} ConfigUrl The url of the resource as read in the 
   *                            configuration file
   * @return {string}           The reconfigured URL.
   * This is a private method (hard to express in JS!?).
   */
  static ReconfigureUrlWithoutPort(ConfigUrl) {
    // The url of the 3DTiles layer as read in the configuration file
    if (!ConfigUrl.includes('DEMO_SERVER')) {
      // Nothing to fix, return the original url
      return ConfigUrl;
    }

    // The url of the server that served this javascript source
    const ServerUrl = `${window.location.protocol}//${window.location.hostname}`;
    // The actual URL of the layer as hosted on the (same) server that
    // delivered this javascript source
    return ConfigUrl.replace('DEMO_SERVER', ServerUrl);
  }

  /**
   * Refer to the documentation of ReconfigureUrlWithoutPort(ConfigUrl)
   * for the role, parameter and return value.
   * This version (as opposed to ReconfigureUrlWithoutPort) DOES include
   * the port number.
   */
  static ReconfigureUrlWithPort(ConfigUrl) {
    // The url of the 3DTiles layer as read in the configuration file
    if (!ConfigUrl.includes('DEMO_SERVER')) {
      // Nothing to fix, return the original url
      return ConfigUrl;
    }

    // The url of the server that served this javascript source
    let ServerUrl = `${window.location.protocol}//${window.location.hostname}`;
    ServerUrl += (window.location.port ? ':' + window.location.port : '');
    // The actual URL of the layer as hosted on the (same) server that
    // delivered this javascript source
    return ConfigUrl.replace('DEMO_SERVER', ServerUrl);
  }

  /**
   * Create an iTowns 3D Tiles layer based on the specified layerConfig.
   * @param {string} layerConfig The name of the layer to setup from the
   * generalDemoConfig.json config file (should be one of the properties
   * of the 3DTilesLayer object in
   * UD-Viz/UD-Viz-Core/examples/data/config/generalDemoConfig.json
   * config file).
   */
  setup3DTilesLayer() {
    //  ADD 3D Tiles Layer

    // Positional arguments verification
    if (!this.config['3DTilesLayer']) {
      throw (
        '3DTilesLayer object cannot be setup without the associated' + 
        'property (refer to your configuration file).'
      );
    }

    if (
      !this.config['3DTilesLayer']['id'] ||
      !this.config['3DTilesLayer']['url']
    ) {
      throw ( "The 3DTiles layer is missing 'url'/'id' properties or both. " );
    }
    
    const extensionsConfig = this.config['3DTilesLayer']['extensions'];
    let extensions = new itowns.C3DTExtensions();
    if (!!extensionsConfig) {
      for (let i = 0; i < extensionsConfig.length; i++) {
        if (extensionsConfig[i] === '3DTILES_temporal') {
          extensions.registerExtension('3DTILES_temporal', {
            [itowns.C3DTilesTypes.batchtable]: $3DTemporalBatchTable,
            [itowns.C3DTilesTypes.boundingVolume]: $3DTemporalBoundingVolume,
            [itowns.C3DTilesTypes.tileset]: $3DTemporalTileset,
          });
        } else if (extensionsConfig[i] === '3DTILES_batch_table_hierarchy') {
          extensions.registerExtension('3DTILES_batch_table_hierarchy', {
            [itowns.C3DTilesTypes.batchtable]:
              itowns.C3DTBatchTableHierarchyExtension,
          });
        } else {
          console.warn(
            'The 3D Tiles extension ' +
            extensionsConfig[i] +
            ' specified in generalDemoConfig.json is not supported ' +
            'by UD-Viz yet. Only 3DTILES_temporal and ' +
            '3DTILES_batch_table_hierarchy are supported.'
          );
        }
      }
    }

    var $3dTilesLayer = new itowns.C3DTilesLayer(
      this.config['3DTilesLayer']['id'],
      {
        name: 'Lyon-2015-'.concat(this.config['3DTilesLayer']['id']),
        source: new itowns.C3DTilesSource({
          url: this.config['3DTilesLayer']['url'],
        }),
        registeredExtensions: extensions,
      },
      this.view
    );

    let material;
    if (this.config['3DTilesLayer']['pc_size']) {
      material = new THREE.PointsMaterial({
        size: this.config['3DTilesLayer']['pc_size'],
        vertexColors: true,
      });
    } else if (!this.config['3DTilesLayer']['color']) {
      material = new THREE.MeshLambertMaterial({ color: 0xffffff });
    } else {
      material = new THREE.MeshLambertMaterial({
        color: parseInt(this.config['3DTilesLayer']['color']),
      });
    }

    $3dTilesLayer.overrideMaterials = material;
    $3dTilesLayer.material = material;

    const $3DTilesManager = new TilesManager(this.view, $3dTilesLayer);
    this.layerManager.tilesManagers.push($3DTilesManager);

    return [$3dTilesLayer, $3DTilesManager];
  }

  /**
   * Adds the specified 3D Tiles layer to the iTowns 3D view.
   * @param {itowns.C3DTilesLayer} layer The layer to add to itowns view.
   */
  add3DTilesLayer(layer) {
    itowns.View.prototype.addLayer.call(this.view, layer);
  }

  /**
   * Sets up a 3D Tiles layer and adds it to the itowns view (for the demos
   * that don't need more granularity than that).
   * @param {string} layerConfig The name of the layer to setup from the
   * generalDemoConfig.json config file (should be one of the properties
   * of the 3DTilesLayer object in
   * UD-Viz/UD-Viz-Core/examples/data/config/generalDemoConfig.json
   * config file).
   */
  setupAndAdd3DTilesLayer() {
    const [$3DTilesLayer] = this.setup3DTilesLayer();
    this.add3DTilesLayer($3DTilesLayer);
  }

  /**
   * Initializes the iTowns 3D view according the config.
   */
  init3DView() {
    // ********* INIT ITOWNS VIEW
    // Define projection used in iTowns viewer (taken from
    // https://epsg.io/3946, Proj4js section)
    proj4.defs(
      'EPSG:3946',
      '+proj=lcc +lat_1=45.25 +lat_2=46.75' +
      ' +lat_0=46 +lon_0=3 +x_0=1700000 +y_0=5200000 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs'
    );

    // Define geographic extent: CRS, min/max X, min/max Y
    // area should be one of the properties of the object extents in config file
    let min_x = parseInt(this.config['extents']['min_x']);
    let max_x = parseInt(this.config['extents']['max_x']);
    let min_y = parseInt(this.config['extents']['min_y']);
    let max_y = parseInt(this.config['extents']['max_y']);
    this.extent = new itowns.Extent(
      this.config['projection'],
      min_x,
      max_x,
      min_y,
      max_y,
    );

    // Get camera placement parameters from config
    let coordinates = this.extent.center();
    if (
      this.config['camera']['position']['x'] &&
      this.config['camera']['position']['y']
    ) {
      coordinates = new itowns.Coordinates(
        'EPSG:3946',
        parseInt(this.config['camera']['position']['x']),
        parseInt(this.config['camera']['position']['y'])
      );
    }
    const heading = parseFloat(this.config['camera']['position']['heading']);
    const range = parseFloat(this.config['camera']['position']['range']);
    const tilt = parseFloat(this.config['camera']['position']['tilt']);

    // `viewerDiv` will contain iTowns' rendering area (`<canvas>`)
    let viewerDiv = document.getElementById('viewerDiv');
    // Instantiate PlanarView (iTowns' view that will hold the layers)
    // The skirt allows to remove the cracks between the terrain tiles
    // Instantiate controls within PlanarView
    this.view = new itowns.PlanarView(viewerDiv, this.extent, {
      disableSkirt: false,
      controls: {
        maxZenithAngle: 180,
        groundLevel: -100,
        handleCollision: false,
      },
      placement: {
        coord: coordinates,
        heading: heading,
        range: range,
        tilt: tilt,
      },
    });

    this.layerManager = new LayerManager(this.view);
    // ********* 3D Elements
    // Lights
    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.5);
    directionalLight.position.set(0, 0, 20000);
    directionalLight.updateMatrixWorld();
    this.view.scene.add(directionalLight);

    const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
    ambientLight.position.set(0, 0, 3000);
    directionalLight.updateMatrixWorld();
    this.view.scene.add(ambientLight);

    // Controls
    this.controls = this.view.controls;

    // Set sky color to blue
    this.view.mainLoop.gfxEngine.renderer.setClearColor(0x6699cc, 1);
  }

  /*
   * Updates the 3D view by notifying iTowns that it changed (e.g. because a layer has been added).
   */
  update3DView() {
    // Request itowns view redraw
    this.view.notifyChange();
  }

  /**
   * Loads a config file. Module views should only be added after calling
   * this method.
   * @param filePath The path to the config file.
   */
  async loadConfigFile(filePath) {
    // Loading configuration file
    // refer to https://github.com/MEPP-team/VCity/wiki/Configuring-UDV
    return jquery.ajax({
      type: 'GET',
      url: filePath,
      datatype: 'json',
      success: (data) => {
        this.config = data;
      },
      error: (e) => {
        throw 'Could not load config file : ' + filePath;
      },
    });
  }

  // /////////////////////////////////////////////////////
  // GETTERS FOR HTML IDS AND ELEMENTS OF THE DEMO PAGE //
  // /////////////////////////////////////////////////////

  get mainDivId() {
    return '_base_demo';
  }

  get headerId() {
    return '_base_demo_header';
  }

  get headerElement() {
    return document.getElementById(this.headerId);
  }

  get authFrameLocationId() {
    return '_base_demo_auth_frame_location';
  }

  get authFrameLocationElement() {
    return document.getElementById(this.authFrameLocationId);
  }

  get contentSectionId() {
    return 'contentSection';
  }

  get contentSectionElement() {
    return document.getElementById(this.contentSectionId);
  }

  get viewerDivId() {
    return 'viewerDiv';
  }

  get viewerDivElement() {
    return document.getElementById(this.viewerDivId);
  }

  get menuId() {
    return '_base_demo_menu';
  }

  get menuElement() {
    return document.getElementById(this.menuId);
  }

  get authenticationFrameId() {
    return '_base_demo_profile';
  }

  get authenticationFrameElement() {
    return document.getElementById(this.authenticationFrameId);
  }

  get authenticationLogoutButtonId() {
    return '_base_demo_button_logout';
  }

  get authenticationLogoutButtonElement() {
    return document.getElementById(this.authenticationLogoutButtonId);
  }

  get authenticationLoginButtonId() {
    return '_base_demo_button_login';
  }

  get authenticationLoginButtonElement() {
    return document.getElementById(this.authenticationLoginButtonId);
  }

  get authenticationMenuLoggedInId() {
    return '_base_demo_profile_menu_logged_in';
  }

  get authenticationMenuLoggedInElement() {
    return document.getElementById(this.authenticationMenuLoggedInId);
  }

  get authenticationMenuLoggedOutId() {
    return '_base_demo_profile_menu_logged_out';
  }

  get authenticationMenuLoggedOutElement() {
    return document.getElementById(this.authenticationMenuLoggedOutId);
  }

  get authenticationUserNameId() {
    return '_base_demo_profile_name';
  }

  get authenticationUserNameElement() {
    return document.getElementById(this.authenticationUserNameId);
  }

  static get MODULE_VIEW() {
    return 'MODULE_VIEW';
  }

  static get AUTHENTICATION_MODULE() {
    return 'AUTHENTICATION_MODULE';
  }
}
