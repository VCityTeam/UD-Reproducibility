import * as THREE from 'three';

export class BillBoard {
  /// Visualize document in the city 3D model of UD-Viz
  // FIXME Why not use a constructor ?
  // FIXME Why are texture, material, sprite...not attributes ? (i.e. you
  // should be using this.texture...)
  CreateBillBoard(image, coord, scale) {
    const texture = new THREE.TextureLoader().load(image);
    const material = new THREE.SpriteMaterial({ map: texture });
    const sprite = new THREE.Sprite(material);
    sprite.position.set(coord.x, coord.y, coord.z);
    sprite.scale.set(scale.x, scale.y, scale.z); // imageWidth, imageHeight
    sprite.updateMatrixWorld();
    return sprite;
  }
}
